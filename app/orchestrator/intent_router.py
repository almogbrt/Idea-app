"""Intent Router: LLM-driven, function-calling based command routing.

There is deliberately no regex, no keyword table, and no if/elif chain of
intents anywhere in this module. The LLM is given the full set of tool
schemas exposed by every registered agent and decides — via native
function/tool calling — which tool(s), if any, to invoke, in a loop until
it produces a final natural-language answer.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.application.ports.agent_execution_repository import AgentExecutionRepositoryPort
from app.application.ports.agent_tool import ToolExecutionContext
from app.application.ports.llm_gateway import LLMGatewayPort, LLMMessage, LLMStopReason
from app.core.exceptions import ExternalServiceError
from app.core.logging import get_logger
from app.domain.entities import AgentExecution, ExecutionStatus, MessageRole, ToolCall, ToolResult
from app.orchestrator.agent_registry import AgentRegistry

logger = get_logger(__name__)

MAX_TOOL_ITERATIONS = 8


@dataclass(slots=True)
class RoutingResult:
    reply: str
    tool_calls_made: list[ToolCall] = field(default_factory=list)
    trace_messages: list[LLMMessage] = field(default_factory=list)
    """The assistant/tool_use + tool/tool_result messages appended during the
    loop, in order. Anthropic's API requires every tool_use block to be
    followed immediately by its tool_result — collapsing a multi-tool-call
    turn into a single summary message (as the caller used to do) breaks
    that invariant the next time this conversation's history is replayed.
    The caller must persist these individually, in order, alongside its own
    final assistant reply message."""


class IntentRouter:
    def __init__(
        self,
        llm_gateway: LLMGatewayPort,
        agent_registry: AgentRegistry,
        agent_execution_repository: AgentExecutionRepositoryPort,
    ) -> None:
        self._llm = llm_gateway
        self._registry = agent_registry
        self._executions = agent_execution_repository

    async def route(
        self,
        *,
        system_prompt: str,
        conversation: list[LLMMessage],
        context: ToolExecutionContext,
    ) -> RoutingResult:
        messages = list(conversation)
        tools = self._registry.all_tool_definitions()
        tool_calls_made: list[ToolCall] = []
        trace_messages: list[LLMMessage] = []

        for iteration in range(MAX_TOOL_ITERATIONS):
            response = await self._llm.generate(
                system_prompt=system_prompt, messages=messages, tools=tools
            )

            if response.stop_reason != LLMStopReason.TOOL_USE:
                return RoutingResult(
                    reply=response.content,
                    tool_calls_made=tool_calls_made,
                    trace_messages=trace_messages,
                )

            if not response.tool_calls:
                logger.warning("tool_use_stop_reason_without_tool_calls", iteration=iteration)
                return RoutingResult(
                    reply=response.content,
                    tool_calls_made=tool_calls_made,
                    trace_messages=trace_messages,
                )

            assistant_message = LLMMessage(
                role=MessageRole.ASSISTANT,
                content=response.content,
                tool_calls=response.tool_calls,
            )
            messages.append(assistant_message)
            trace_messages.append(assistant_message)

            for call in response.tool_calls:
                result = await self._execute_tool(call, context)
                tool_calls_made.append(call)
                tool_message = LLMMessage(
                    role=MessageRole.TOOL,
                    content=result.content,
                    tool_call_id=call.id,
                )
                messages.append(tool_message)
                trace_messages.append(tool_message)

        logger.error("max_tool_iterations_exceeded", conversation_id=str(context.conversation_id))
        raise ExternalServiceError(
            "Edith could not complete the request within the allowed tool-call budget."
        )

    async def _execute_tool(self, call: ToolCall, context: ToolExecutionContext) -> ToolResult:
        tool = self._registry.get_tool(call.tool_name)
        started = time.monotonic()
        try:
            result = await tool.execute(call.arguments, context)
            status = ExecutionStatus.ERROR if result.is_error else ExecutionStatus.SUCCESS
        except Exception as exc:  # noqa: BLE001 - tool failures must not crash the loop
            logger.error("tool_execution_failed", tool=call.tool_name, error=str(exc))
            result = ToolResult(
                tool_call_id=call.id,
                tool_name=call.tool_name,
                content=f"Tool '{call.tool_name}' failed: {exc}",
                is_error=True,
            )
            status = ExecutionStatus.ERROR
        latency_ms = int((time.monotonic() - started) * 1000)

        await self._executions.record(
            AgentExecution(
                id=uuid.uuid4(),
                user_id=context.user_id,
                agent_name=tool.agent_name,
                tool_name=call.tool_name,
                input=call.arguments,
                output={"content": result.content, "is_error": result.is_error},
                status=status,
                latency_ms=latency_ms,
                created_at=datetime.now(UTC),
            )
        )
        return result
