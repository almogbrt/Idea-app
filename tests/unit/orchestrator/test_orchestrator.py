from __future__ import annotations

import uuid

from app.application.ports.llm_gateway import LLMResponse, LLMStopReason
from app.application.use_cases.memory_use_cases import RetrieveMemoryUseCase, StoreMemoryUseCase
from app.domain.entities import MessageRole
from app.orchestrator.agent_registry import AgentRegistry
from app.orchestrator.intent_router import IntentRouter
from app.orchestrator.orchestrator import Orchestrator
from tests.conftest import (
    FakeAgentExecutionRepository,
    FakeConversationRepository,
    FakeEmbeddingGateway,
    FakeMemoryRepository,
    ScriptedLLMGateway,
)


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

    assert len(fake_memory_repository.records) == 1
    assert fake_memory_repository.records[0].content == "remember this fact"
