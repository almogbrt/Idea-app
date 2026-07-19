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


class ProjectStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    DONE = "done"


class TaskStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class NotificationKind(StrEnum):
    TASK_DUE_SOON = "task_due_soon"
    TASK_OVERDUE = "task_overdue"
    CLIENT_FOLLOW_UP_DUE = "client_follow_up_due"


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
    tool_call_id: str | None = None
    """Set when role == TOOL: which tool call this message is a result for."""


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
class Client:
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    created_at: datetime
    email: str | None = None
    phone: str | None = None
    notes: str | None = None
    next_follow_up_at: datetime | None = None


@dataclass(slots=True)
class Project:
    id: uuid.UUID
    user_id: uuid.UUID
    client_id: uuid.UUID | None
    name: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class Task:
    id: uuid.UUID
    user_id: uuid.UUID
    project_id: uuid.UUID | None
    title: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    due_at: datetime | None = None
    client_id: uuid.UUID | None = None
    """Direct client association — independent of `project_id`, since not
    every client-related task belongs to a project."""


@dataclass(slots=True)
class ProjectSummary:
    """A `Project` enriched with denormalized fields for the dashboard table,
    so the UI doesn't need a second round trip to resolve names."""

    project: Project
    client_name: str | None
    last_task_title: str | None


@dataclass(slots=True)
class ClientDetail:
    """A `Client` plus its full history, for the CRM detail view."""

    client: Client
    projects: list[ProjectSummary]
    tasks: list[Task]


@dataclass(slots=True)
class CalendarEvent:
    """A Google Calendar event, for the dashboard calendar view — not
    persisted locally, Google Calendar is the source of truth."""

    id: str
    summary: str
    start: str
    """ISO 8601 datetime string, as returned by the Calendar API."""
    end: str
    description: str | None = None
    html_link: str | None = None


@dataclass(slots=True)
class DriveFile:
    """A Google Drive file, for the dashboard files view — not persisted
    locally, Drive is the source of truth."""

    id: str
    name: str
    mime_type: str
    web_view_link: str | None = None
    modified_time: str | None = None


@dataclass(slots=True)
class Notification:
    """A reminder surfaced in the dashboard bell (and mirrored by email).
    `related_id` points at the `Task` or `Client` that triggered it, depending
    on `kind`."""

    id: uuid.UUID
    user_id: uuid.UUID
    kind: NotificationKind
    related_id: uuid.UUID
    title: str
    body: str
    created_at: datetime
    read_at: datetime | None = None


@dataclass(slots=True)
class OrchestrationResult:
    """The final answer returned to the caller, plus the audit trail."""

    reply: str
    conversation_id: uuid.UUID
    tool_calls_made: list[ToolCall] = field(default_factory=list)
