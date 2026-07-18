from __future__ import annotations

import uuid
from typing import Any

import pytest

from app.application.ports.agent_tool import Tool, ToolExecutionContext
from app.application.ports.llm_gateway import LLMMessage, LLMResponse, LLMStopReason
from app.core.exceptions import ExternalServiceError
from app.domain.entities import ExecutionStatus, MessageRole, ToolCall, ToolResult
from app.orchestrator.agent_registry import AgentRegistry
from app.orchestrator.base_agent import BaseAgent
from app.orchestrator.intent_router import MAX_TOOL_ITERATIONS, IntentRouter
from tests.conftest import FakeAgentExecutionRepository, ScriptedLLMGateway


class _WeatherTool(Tool):
    name = "get_weather"
    description = "Gets the weather"
    parameters_schema: dict[str, Any] = {"type": "object", "properties": {}}
    agent_name = "weather"

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        return ToolResult(tool_call_id="", tool_name=self.name, content="sunny, 25C")


class _FailingTool(Tool):
    name = "flaky_tool"
    description = "Always fails"
    parameters_schema: dict[str, Any] = {"type": "object", "properties": {}}
    agent_name = "flaky"

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        raise RuntimeError("boom")


class _WeatherAgent(BaseAgent):
    name = "weather"
    description = "weather agent"

    def get_tools(self) -> list[Tool]:
        return [_WeatherTool(), _FailingTool()]


@pytest.fixture
def registry() -> AgentRegistry:
    registry = AgentRegistry()
    registry.register(_WeatherAgent())
    return registry


@pytest.fixture
def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        user_id=uuid.uuid4(), conversation_id=uuid.uuid4(), correlation_id="test-correlation"
    )


async def test_returns_immediately_on_end_turn(
    registry: AgentRegistry,
    context: ToolExecutionContext,
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> None:
    llm = ScriptedLLMGateway(
        responses=[
            LLMResponse(content="Hello there!", tool_calls=(), stop_reason=LLMStopReason.END_TURN)
        ]
    )
    router = IntentRouter(llm, registry, fake_agent_execution_repository)

    result = await router.route(
        system_prompt="system",
        conversation=[LLMMessage(role=MessageRole.USER, content="hi")],
        context=context,
    )

    assert result.reply == "Hello there!"
    assert result.tool_calls_made == []
    assert len(llm.calls) == 1


async def test_executes_tool_then_returns_final_reply(
    registry: AgentRegistry,
    context: ToolExecutionContext,
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> None:
    call = ToolCall(id="call-1", tool_name="get_weather", arguments={})
    llm = ScriptedLLMGateway(
        responses=[
            LLMResponse(content="", tool_calls=(call,), stop_reason=LLMStopReason.TOOL_USE),
            LLMResponse(content="It's sunny!", tool_calls=(), stop_reason=LLMStopReason.END_TURN),
        ]
    )
    router = IntentRouter(llm, registry, fake_agent_execution_repository)

    result = await router.route(
        system_prompt="system",
        conversation=[LLMMessage(role=MessageRole.USER, content="what's the weather?")],
        context=context,
    )

    assert result.reply == "It's sunny!"
    assert len(result.tool_calls_made) == 1
    assert result.tool_calls_made[0].tool_name == "get_weather"
    assert len(fake_agent_execution_repository.executions) == 1
    execution = fake_agent_execution_repository.executions[0]
    assert execution.status == ExecutionStatus.SUCCESS
    assert execution.tool_name == "get_weather"

    # the second LLM call should have seen the tool result as a TOOL message
    second_call_messages = llm.calls[1]["messages"]
    assert any(m.role == MessageRole.TOOL and "sunny" in m.content for m in second_call_messages)

    # trace_messages must carry the granular assistant/tool_use + tool/tool_result
    # pair the caller needs to persist individually — collapsing this into one
    # summary message breaks conversation history on the next turn (each
    # tool_use must be immediately followed by its tool_result).
    assert [m.role for m in result.trace_messages] == [MessageRole.ASSISTANT, MessageRole.TOOL]
    assert result.trace_messages[0].tool_calls == (call,)
    assert result.trace_messages[1].tool_call_id == "call-1"


async def test_tool_execution_failure_is_recorded_and_fed_back_to_llm(
    registry: AgentRegistry,
    context: ToolExecutionContext,
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> None:
    call = ToolCall(id="call-1", tool_name="flaky_tool", arguments={})
    llm = ScriptedLLMGateway(
        responses=[
            LLMResponse(content="", tool_calls=(call,), stop_reason=LLMStopReason.TOOL_USE),
            LLMResponse(
                content="Something went wrong.",
                tool_calls=(),
                stop_reason=LLMStopReason.END_TURN,
            ),
        ]
    )
    router = IntentRouter(llm, registry, fake_agent_execution_repository)

    result = await router.route(
        system_prompt="system",
        conversation=[LLMMessage(role=MessageRole.USER, content="do the flaky thing")],
        context=context,
    )

    assert result.reply == "Something went wrong."
    execution = fake_agent_execution_repository.executions[0]
    assert execution.status == ExecutionStatus.ERROR


async def test_raises_when_max_tool_iterations_exceeded(
    registry: AgentRegistry,
    context: ToolExecutionContext,
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> None:
    call = ToolCall(id="call-1", tool_name="get_weather", arguments={})
    always_tool_use = [
        LLMResponse(content="", tool_calls=(call,), stop_reason=LLMStopReason.TOOL_USE)
        for _ in range(MAX_TOOL_ITERATIONS + 1)
    ]
    llm = ScriptedLLMGateway(responses=always_tool_use)
    router = IntentRouter(llm, registry, fake_agent_execution_repository)

    with pytest.raises(ExternalServiceError):
        await router.route(
            system_prompt="system",
            conversation=[LLMMessage(role=MessageRole.USER, content="loop forever")],
            context=context,
        )
