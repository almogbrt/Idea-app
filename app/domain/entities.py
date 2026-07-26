"""Domain entities.

These are plain, framework-free data structures. They know nothing about
FastAPI, SQLAlchemy, or any LLM SDK — infrastructure adapters translate to
and from these types at the boundary.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
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


class ProjectType(StrEnum):
    CONSULTING = "consulting"
    MENTORING = "mentoring"
    SETUP = "setup"


class TaskStatus(StrEnum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskImportance(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCategory(StrEnum):
    MANAGERIAL = "managerial"
    OPERATIONAL = "operational"


class FocusExitReason(StrEnum):
    DONE = "done"
    STUCK = "stuck"
    BREAK = "break"


class FocusStuckReason(StrEnum):
    UNCLEAR = "unclear"
    TOO_BIG = "too_big"
    BLOCKED = "blocked"
    DISTRACTED = "distracted"


class NotificationKind(StrEnum):
    TASK_DUE_SOON = "task_due_soon"
    TASK_OVERDUE = "task_overdue"
    TASK_ENDING_SOON = "task_ending_soon"
    TASK_TIMER_EXPIRED = "task_timer_expired"
    CALENDAR_EVENT_STARTING = "calendar_event_starting"
    DAILY_REVIEW = "daily_review"


class WhatsAppDirection(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


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
    logo_file_id: str | None = None
    """Google Drive file id of the client's logo image, if one was uploaded."""


@dataclass(slots=True)
class ClientAttachment:
    """A document or image uploaded for a client — stored in the user's own
    Google Drive (via `file_id`), tracked here just so it can be listed and
    fetched per-client rather than searched for in Drive."""

    id: uuid.UUID
    user_id: uuid.UUID
    client_id: uuid.UUID
    file_id: str
    filename: str
    mime_type: str
    created_at: datetime


@dataclass(slots=True)
class Project:
    id: uuid.UUID
    user_id: uuid.UUID
    client_id: uuid.UUID | None
    name: str
    type: ProjectType
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
    start_at: datetime | None = None
    """When work on the task is scheduled to begin. Required (alongside
    `due_at`, its end time) when a task is created through the normal
    creation paths — nullable here only so older rows created before this
    field existed keep loading."""
    timer_started_at: datetime | None = None
    """Set when the user actually clicks "start" on the task (not the same
    as `start_at`, the originally planned start time). The timer's duration
    is `due_at - start_at`; `timer_started_at + that duration` is the
    countdown deadline, timed from when work actually began."""
    deliverable: str | None = None
    """What "done" looks like for this task — set when picked as one of a
    day's 3 outcomes in the My Day flow."""
    estimated_minutes: int | None = None
    """Estimated effort in minutes, set alongside `deliverable` — drives the
    Focus-mode timer, independent of `start_at`/`due_at`/`timer_started_at`
    (those remain the general task-list's own scheduling/timer feature)."""
    importance: TaskImportance | None = None
    goal_id: uuid.UUID | None = None
    next_step: str | None = None
    """Free-text note on what to do next — shown/edited in Focus mode."""
    category: TaskCategory | None = None
    """Managerial vs. operational — decides which dashboard window the task
    lives in. `None` only for tasks created before this field existed (or
    via the Inbox quick-capture path); the dashboard shows those in a
    dedicated "needs classification" bucket until the user picks one."""


@dataclass(slots=True)
class Goal:
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    created_at: datetime


@dataclass(slots=True)
class DailyPlan:
    id: uuid.UUID
    user_id: uuid.UUID
    plan_date: date
    main_task_id: uuid.UUID | None
    secondary_task_id_1: uuid.UUID | None
    secondary_task_id_2: uuid.UUID | None
    is_locked: bool
    locked_at: datetime | None
    carry_over_task_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class FocusSession:
    id: uuid.UUID
    user_id: uuid.UUID
    task_id: uuid.UUID
    daily_plan_id: uuid.UUID
    started_at: datetime
    ended_at: datetime | None = None
    exit_reason: FocusExitReason | None = None
    stuck_reason: FocusStuckReason | None = None


@dataclass(slots=True)
class DailyPlanSwap:
    id: uuid.UUID
    user_id: uuid.UUID
    daily_plan_id: uuid.UUID
    bumped_task_id: uuid.UUID | None
    """Nullable so the audit log survives the referenced task being deleted
    later (`ON DELETE SET NULL`) — the swap count itself is what matters for
    metrics, not a live reference."""
    new_task_id: uuid.UUID | None
    created_at: datetime


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
    attachments: list[ClientAttachment]


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
class EmailSummary:
    """A Gmail message summary, for the dashboard inbox view — not persisted
    locally, Gmail is the source of truth."""

    id: str
    sender: str
    subject: str
    snippet: str
    date: str


@dataclass(slots=True)
class Thought:
    """A quick, freeform jotted-down idea — typed or dictated, not tied to
    any client/project/task. The in-house replacement for a third-party
    handwriting-notes app, since we can't reliably deep-link into one."""

    id: uuid.UUID
    user_id: uuid.UUID
    content: str
    created_at: datetime


@dataclass(slots=True)
class WhatsAppMessage:
    """One message sent or received over the business WhatsApp number.
    `phone_number` is always the *other* party (a client, or the owner's own
    personal number when they're commanding Edith directly) — there's only
    ever one business number, so it isn't stored per-message."""

    id: uuid.UUID
    user_id: uuid.UUID
    phone_number: str
    direction: WhatsAppDirection
    content: str
    created_at: datetime


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
class IncomeRecord:
    """One income document (invoice/receipt) from Green Invoice — read-only,
    not persisted locally, Green Invoice is the source of truth."""

    id: str
    date: str
    """ISO 8601 date string, as returned by the Green Invoice API."""
    amount: float
    currency: str
    client_name: str | None
    description: str | None
    status: str
    green_invoice_client_id: str | None = None
    """Green Invoice's own client id — a stable key for manual client
    linking, unlike `client_name` which breaks if the client is renamed."""
    matched_client_id: uuid.UUID | None = None


@dataclass(slots=True)
class ExpenseRecord:
    """One expense record from Green Invoice — read-only, not persisted
    locally, Green Invoice is the source of truth."""

    id: str
    date: str
    amount: float
    currency: str
    category: str | None
    description: str | None


@dataclass(slots=True)
class FinanceOverview:
    """Aggregated income/expense view for the dashboard finance section, for
    a given date range."""

    from_date: date
    to_date: date
    income: list[IncomeRecord]
    expenses: list[ExpenseRecord]
    total_income: float
    total_expenses: float
    net: float


@dataclass(slots=True)
class CashFlowSnapshot:
    """A snapshot of a few key numbers read from a dedicated tab in the
    user's own cash-flow Google Sheet — not persisted locally, the sheet is
    the source of truth."""

    current_balance: float
    fixed_expenses_this_month: float
    dues_this_month: float
    projected_end_of_month_balance: float
    fetched_at: datetime


@dataclass(slots=True)
class OrchestrationResult:
    """The final answer returned to the caller, plus the audit trail."""

    reply: str
    conversation_id: uuid.UUID
    tool_calls_made: list[ToolCall] = field(default_factory=list)
