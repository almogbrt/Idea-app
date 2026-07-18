from __future__ import annotations

import asyncio
import uuid
from typing import Any

from app.application.ports.agent_tool import Tool, ToolExecutionContext
from app.application.ports.embedding import EmbeddingPort
from app.application.ports.llm_gateway import LLMMessage, LLMResponse, LLMStopReason
from app.application.use_cases.memory_use_cases import RetrieveMemoryUseCase, StoreMemoryUseCase
from app.core.exceptions import ExternalServiceError
from app.domain.entities import MessageRole, ToolCall, ToolResult
from app.orchestrator.agent_registry import AgentRegistry
from app.orchestrator.base_agent import BaseAgent
from app.orchestrator.intent_router import IntentRouter
from app.orchestrator.orchestrator import Orchestrator
from tests.conftest import (
    FakeAgentExecutionRepository,
    FakeConversationRepository,
    FakeEmbeddingGateway,
    FakeMemoryRepository,
    ScriptedLLMGateway,
)


class _EchoTool(Tool):
    name = "echo"
    description = "Echoes back"
    parameters_schema: dict[str, Any] = {"type": "object", "properties": {}}
    agent_name = "echo"

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        return ToolResult(tool_call_id="", tool_name=self.name, content="echoed")


class _EchoAgent(BaseAgent):
    name = "echo"
    description = "echo agent"

    def get_tools(self) -> list[Tool]:
        return [_EchoTool()]


class _FailingEmbeddingGateway(EmbeddingPort):
    async def embed(self, text: str) -> list[float]:
        raise ExternalServiceError("OpenAI embeddings API error: Connection error.")


async def _build_orchestrator(
    reply: str,
    fake_conversation_repository: FakeConversationRepository,
    fake_memory_repository: FakeMemoryRepository,
    fake_embedding_gateway: FakeEmbeddingGateway,
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> Orchestrator:
    llm = ScriptedLLMGateway(
        responses=[LLMResponse(content=reply, tool_calls=(), stop_reason=LLMStopReason.END_TURN)]
    )
    router = IntentRouter(llm, AgentRegistry(), fake_agent_execution_repository)
    retrieve_memory = RetrieveMemoryUseCase(fake_embedding_gateway, fake_memory_repository)
    store_memory = StoreMemoryUseCase(fake_embedding_gateway, fake_memory_repository)
    return Orchestrator(fake_conversation_repository, router, retrieve_memory, store_memory)


async def test_handle_command_persists_user_and_assistant_messages(
    fake_conversation_repository: FakeConversationRepository,
    fake_memory_repository: FakeMemoryRepository,
    fake_embedding_gateway: FakeEmbeddingGateway,
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> None:
    orchestrator = await _build_orchestrator(
        "Sure, done!",
        fake_conversation_repository,
        fake_memory_repository,
        fake_embedding_gateway,
        fake_agent_execution_repository,
    )
    user_id = uuid.uuid4()
    conversation = await fake_conversation_repository.create_conversation(user_id, "test")

    result = await orchestrator.handle_command(
        user_id=user_id, conversation_id=conversation.id, text="do the thing"
    )

    assert result.reply == "Sure, done!"
    messages = fake_conversation_repository.messages[conversation.id]
    assert [m.role for m in messages] == [MessageRole.USER, MessageRole.ASSISTANT]
    assert messages[0].content == "do the thing"
    assert messages[1].content == "Sure, done!"


async def test_handle_command_stores_the_command_as_long_term_memory(
    fake_conversation_repository: FakeConversationRepository,
    fake_memory_repository: FakeMemoryRepository,
    fake_embedding_gateway: FakeEmbeddingGateway,
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> None:
    orchestrator = await _build_orchestrator(
        "ok",
        fake_conversation_repository,
        fake_memory_repository,
        fake_embedding_gateway,
        fake_agent_execution_repository,
    )
    user_id = uuid.uuid4()
    conversation = await fake_conversation_repository.create_conversation(user_id, "test")

    await orchestrator.handle_command(
        user_id=user_id, conversation_id=conversation.id, text="remember this fact"
    )
    # storing to memory is fired in the background, not awaited inline —
    # give the event loop a turn to run it before asserting.
    await asyncio.sleep(0)

    assert len(fake_memory_repository.records) == 1
    assert fake_memory_repository.records[0].content == "remember this fact"


async def test_handle_command_survives_a_down_embeddings_provider(
    fake_conversation_repository: FakeConversationRepository,
    fake_memory_repository: FakeMemoryRepository,
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> None:
    """Long-term memory is an enhancement, not a hard dependency — Edith must
    still answer even if the embeddings provider is unreachable."""
    llm = ScriptedLLMGateway(
        responses=[
            LLMResponse(content="Still here!", tool_calls=(), stop_reason=LLMStopReason.END_TURN)
        ]
    )
    router = IntentRouter(llm, AgentRegistry(), fake_agent_execution_repository)
    failing_embeddings = _FailingEmbeddingGateway()
    retrieve_memory = RetrieveMemoryUseCase(failing_embeddings, fake_memory_repository)
    store_memory = StoreMemoryUseCase(failing_embeddings, fake_memory_repository)
    orchestrator = Orchestrator(fake_conversation_repository, router, retrieve_memory, store_memory)

    user_id = uuid.uuid4()
    conversation = await fake_conversation_repository.create_conversation(user_id, "test")

    result = await orchestrator.handle_command(
        user_id=user_id, conversation_id=conversation.id, text="hello"
    )

    assert result.reply == "Still here!"
    assert fake_memory_repository.records == []


async def test_a_tool_call_turn_persists_a_history_the_next_turn_can_replay(
    fake_conversation_repository: FakeConversationRepository,
    fake_memory_repository: FakeMemoryRepository,
    fake_embedding_gateway: FakeEmbeddingGateway,
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> None:
    """Regression test: collapsing a tool-call turn into one summary message
    (instead of persisting the granular assistant/tool_use + tool/tool_result
    messages) used to leave a tool_use with no following tool_result once
    that history was replayed on the next command — Anthropic's API rejects
    that shape outright with a 400. This must not happen again."""
    registry = AgentRegistry()
    registry.register(_EchoAgent())
    call = ToolCall(id="call-1", tool_name="echo", arguments={})
    llm = ScriptedLLMGateway(
        responses=[
            LLMResponse(content="", tool_calls=(call,), stop_reason=LLMStopReason.TOOL_USE),
            LLMResponse(content="Echoed it!", tool_calls=(), stop_reason=LLMStopReason.END_TURN),
            LLMResponse(content="Second reply", tool_calls=(), stop_reason=LLMStopReason.END_TURN),
        ]
    )
    router = IntentRouter(llm, registry, fake_agent_execution_repository)
    retrieve_memory = RetrieveMemoryUseCase(fake_embedding_gateway, fake_memory_repository)
    store_memory = StoreMemoryUseCase(fake_embedding_gateway, fake_memory_repository)
    orchestrator = Orchestrator(fake_conversation_repository, router, retrieve_memory, store_memory)

    user_id = uuid.uuid4()
    conversation = await fake_conversation_repository.create_conversation(user_id, "test")

    first = await orchestrator.handle_command(
        user_id=user_id, conversation_id=conversation.id, text="use the echo tool"
    )
    assert first.reply == "Echoed it!"

    messages = fake_conversation_repository.messages[conversation.id]
    assert [m.role for m in messages] == [
        MessageRole.USER,
        MessageRole.ASSISTANT,
        MessageRole.TOOL,
        MessageRole.ASSISTANT,
    ]
    assert messages[1].tool_calls == [call]  # the tool_use message
    assert messages[2].tool_call_id == "call-1"  # its matching tool_result

    # A second command in the same conversation must succeed — it replays the
    # history above back to the LLM, which is where the bug used to surface.
    second = await orchestrator.handle_command(
        user_id=user_id, conversation_id=conversation.id, text="what did you just do?"
    )
    assert second.reply == "Second reply"

    third_call_messages: list[LLMMessage] = llm.calls[2]["messages"]
    for i, message in enumerate(third_call_messages):
        if message.role == MessageRole.ASSISTANT and message.tool_calls:
            assert i + 1 < len(third_call_messages)
            assert third_call_messages[i + 1].role == MessageRole.TOOL
