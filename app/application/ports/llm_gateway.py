"""Port for LLM providers used by the Intent Router.

Any provider (Anthropic, OpenAI, ...) is adapted to this interface in
`app/infrastructure/llm/`. The orchestrator and intent router depend only
on this contract, never on a concrete SDK — swapping providers means
writing one new adapter, not touching routing logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from app.domain.entities import MessageRole, ToolCall, ToolDefinition


@dataclass(frozen=True, slots=True)
class LLMMessage:
    role: MessageRole
    content: str
    tool_calls: tuple[ToolCall, ...] = field(default_factory=tuple)
    tool_call_id: str | None = None
    """Set when role == TOOL: which tool call this message is a result for."""


class LLMStopReason(StrEnum):
    END_TURN = "end_turn"
    TOOL_USE = "tool_use"
    MAX_TOKENS = "max_tokens"


@dataclass(frozen=True, slots=True)
class LLMResponse:
    content: str
    tool_calls: tuple[ToolCall, ...]
    stop_reason: LLMStopReason
    raw_usage: dict[str, Any] = field(default_factory=dict)


class LLMGatewayPort(ABC):
    """Function-calling capable chat completion port. No regex, no keyword matching."""

    @abstractmethod
    async def generate(
        self,
        *,
        system_prompt: str,
        messages: list[LLMMessage],
        tools: list[ToolDefinition],
    ) -> LLMResponse:
        """Send a conversation + available tool schemas, get back either a
        final natural-language reply or a set of tool calls to execute."""
        raise NotImplementedError
