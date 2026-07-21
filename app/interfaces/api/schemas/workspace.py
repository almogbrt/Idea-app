from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.entities import NotificationKind, ProjectType, TaskStatus


class ClientView(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime
    email: str | None = None
    phone: str | None = None
    notes: str | None = None
    has_logo: bool = False


class ClientAttachmentView(BaseModel):
    id: uuid.UUID
    filename: str
    mime_type: str
    created_at: datetime


class CreateClientRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class UpdateClientRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = None
    phone: str | None = None
    notes: str | None = None


class ProjectView(BaseModel):
    id: uuid.UUID
    name: str
    type: ProjectType
    client_id: uuid.UUID | None
    client_name: str | None
    last_task_title: str | None
    created_at: datetime
    updated_at: datetime


class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    client_id: uuid.UUID | None = None
    type: ProjectType | None = None


class UpdateProjectTypeRequest(BaseModel):
    type: ProjectType


class AssignProjectClientRequest(BaseModel):
    client_id: uuid.UUID


class TaskView(BaseModel):
    id: uuid.UUID
    title: str
    status: TaskStatus
    project_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
    due_at: datetime | None = None
    client_id: uuid.UUID | None = None
    start_at: datetime | None = None


class CreateTaskRequest(BaseModel):
    """start_at/due_at are optional here at the schema level — the use case
    is the single place that enforces both being required for new tasks, so
    every entry point (dashboard, chat) is held to the same rule."""

    title: str = Field(..., min_length=1, max_length=500)
    project_id: uuid.UUID | None = None
    due_at: datetime | None = None
    client_id: uuid.UUID | None = None
    start_at: datetime | None = None


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatus


class UpdateTaskRequest(BaseModel):
    """A full-form save (edit modal) — every field is set exactly to what's
    given, not a partial patch. Unlike creation, editing does not force
    adding a start/end time to a task that never had one."""

    title: str = Field(..., min_length=1, max_length=500)
    due_at: datetime | None = None
    project_id: uuid.UUID | None = None
    client_id: uuid.UUID | None = None
    start_at: datetime | None = None


class ThoughtView(BaseModel):
    id: uuid.UUID
    content: str
    created_at: datetime


class CreateThoughtRequest(BaseModel):
    content: str = Field(..., min_length=1)


class ClientDetailView(BaseModel):
    client: ClientView
    projects: list[ProjectView]
    tasks: list[TaskView]
    attachments: list[ClientAttachmentView]


class DashboardSummaryView(BaseModel):
    open_tasks: int
    active_projects: int
    total_clients: int
    unread_emails: int | None
    meetings_today: int | None


class ActivityItemView(BaseModel):
    id: uuid.UUID
    agent_name: str
    tool_name: str
    status: str
    created_at: datetime


class NotificationView(BaseModel):
    id: uuid.UUID
    kind: NotificationKind
    related_id: uuid.UUID
    title: str
    body: str
    created_at: datetime
    read_at: datetime | None


class RunRemindersResponse(BaseModel):
    notifications_raised: int
