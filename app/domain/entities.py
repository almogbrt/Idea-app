"""Domain entities.

These are plain, framework-free data structures. They know nothing about
FastAPI, SQLAlchemy, or any LLM SDK — infrastructure adapters translate to
and from these types at the boundary.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ExecutionStatus(StrEnum):
    SUCCESS = "success"
    ERROR = "error"


@dataclass(slots=True)
class User:
    id: uuid.UUID
    google_sub: str
    email: str
    name: str
    created_at: datetime


@dataclass(slots=True)
class Conversation:
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime


@dataclass(slots=True)
class ToolCall:
    """A single tool invocation requested by the LLM."""

    id: str
    tool_name: str
    arguments: dict[str, Any]


@dataclass(slots=True)
class ToolResult:
    tool_call_id: str
    tool_name: str
    content: str
    is_error: bool = False


@dataclass(slots=True)
class Message:
    id: uuid.UUID
    conversation_id: uuid.UUID
    role: MessageRole
    content: str
    created_at: datetime
    tool_calls: list[ToolCall] = field(default_factory=list)


@dataclass(slots=True)
class ToolDefinition:
    """Describes a callable tool to the LLM (JSON Schema parameters)."""

    name: str
    description: str
    parameters_schema: dict[str, Any]
    agent_name: str


@dataclass(slots=True)
class MemoryRecord:
    id: uuid.UUID
    user_id: uuid.UUID
    content: str
    metadata: dict[str, Any]
    created_at: datetime
    embedding: list[float] | None = None
    similarity: float | None = None


@dataclass(slots=True)
class AgentExecution:
    """Audit record of one tool invocation, for enterprise traceability."""

    id: uuid.UUID
    user_id: uuid.UUID
    agent_name: str
    tool_name: str
    input: dict[str, Any]
    output: dict[str, Any]
    status: ExecutionStatus
    latency_ms: int
    created_at: datetime


@dataclass(slots=True)
class OrchestrationResult:
    """The final answer returned to the caller, plus the audit trail."""

    reply: str
    conversation_id: uuid.UUID
    tool_calls_made: list[ToolCall] = field(default_factory=list)
