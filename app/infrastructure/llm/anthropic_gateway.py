"""Anthropic Claude adapter for `LLMGatewayPort`.

Translates our provider-agnostic message/tool model to and from the Claude
Messages API's native tool-use format. This is the only place in the
codebase that knows Anthropic's wire format.
"""

from __future__ import annotations

from typing import Any, cast

import anthropic
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.application.ports.llm_gateway import (
    LLMGatewayPort,
    LLMMessage,
    LLMResponse,
    LLMStopReason,
)
from app.core.exceptions import ExternalServiceError
from app.core.logging import get_logger
from app.domain.entities import MessageRole, ToolCall, ToolDefinition

logger = get_logger(__name__)

_RETRYABLE_EXCEPTIONS = (
    anthropic.APIConnectionError,
    anthropic.RateLimitError,
    anthropic.InternalServerError,
)

_STOP_REASON_MAP = {
    "tool_use": LLMStopReason.TOOL_USE,
    "end_turn": LLMStopReason.END_TURN,
    "stop_sequence": LLMStopReason.END_TURN,
    "max_tokens": LLMStopReason.MAX_TOKENS,
}


class AnthropicLLMGateway(LLMGatewayPort):
    def __init__(self, api_key: str, model: str, max_tokens: int = 4096) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model
        self._max_tokens = max_tokens

    async def generate(
        self,
        *,
        system_prompt: str,
        messages: list[LLMMessage],
        tools: list[ToolDefinition],
    ) -> LLMResponse:
        anthropic_messages = [
            self._to_anthropic_message(m) for m in messages if m.role != MessageRole.SYSTEM
        ]
        anthropic_tools = [self._to_anthropic_tool(t) for t in tools]

        try:
            response = await self._call_with_retry(
                system=system_prompt, messages=anthropic_messages, tools=anthropic_tools
            )
        except anthropic.APIError as exc:
            logger.error("anthropic_api_error", error=str(exc))
            raise ExternalServiceError(f"Anthropic API error: {exc}") from exc

        return self._to_llm_response(response)

    @retry(
        retry=retry_if_exception_type(_RETRYABLE_EXCEPTIONS),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _call_with_retry(
        self, *, system: str, messages: list[dict[str, Any]], tools: list[dict[str, Any]]
    ) -> anthropic.types.Message:
        kwargs: dict[str, Any] = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
        return cast(anthropic.types.Message, await self._client.messages.create(**kwargs))

    @staticmethod
    def _to_anthropic_tool(tool: ToolDefinition) -> dict[str, Any]:
        return {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.parameters_schema,
        }

    @staticmethod
    def _to_anthropic_message(message: LLMMessage) -> dict[str, Any]:
        if message.role == MessageRole.TOOL:
            return {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": message.tool_call_id,
                        "content": message.content,
                    }
                ],
            }

        if message.role == MessageRole.ASSISTANT and message.tool_calls:
            content: list[dict[str, Any]] = []
            if message.content:
                content.append({"type": "text", "text": message.content})
            content.extend(
                {"type": "tool_use", "id": call.id, "name": call.tool_name, "input": call.arguments}
                for call in message.tool_calls
            )
            return {"role": "assistant", "content": content}

        role = "assistant" if message.role == MessageRole.ASSISTANT else "user"
        return {"role": role, "content": message.content}

    @staticmethod
    def _to_llm_response(response: anthropic.types.Message) -> LLMResponse:
        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(id=block.id, tool_name=block.name, arguments=dict(block.input))
                )

        stop_reason = _STOP_REASON_MAP.get(
            response.stop_reason or "end_turn", LLMStopReason.END_TURN
        )
        return LLMResponse(
            content="\n".join(text_parts),
            tool_calls=tuple(tool_calls),
            stop_reason=stop_reason,
            raw_usage=response.usage.model_dump() if response.usage else {},
        )
