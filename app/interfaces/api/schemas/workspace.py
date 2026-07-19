from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.entities import NotificationKind, ProjectStatus, TaskStatus


class ClientView(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime
    email: str | None = None
    phone: str | None = None
    notes: str | None = None
    next_follow_up_at: datetime | None = None


class CreateClientRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class UpdateClientRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    email: str | None = None
    phone: str | None = None
    notes: str | None = None
    next_follow_up_at: datetime | None = None


class ProjectView(BaseModel):
    id: uuid.UUID
    name: str
    status: ProjectStatus
    client_id: uuid.UUID | None
    client_name: str | None
    last_task_title: str | None
    created_at: datetime
    updated_at: datetime


class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    client_id: uuid.UUID | None = None


class UpdateProjectStatusRequest(BaseModel):
    status: ProjectStatus


class TaskView(BaseModel):
    id: uuid.UUID
    title: str
    status: TaskStatus
    project_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
    due_at: datetime | None = None


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    project_id: uuid.UUID | None = None
    due_at: datetime | None = None


class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatus


class UpdateTaskDueAtRequest(BaseModel):
    due_at: datetime | None = None


class ClientDetailView(BaseModel):
    client: ClientView
    projects: list[ProjectView]
    tasks: list[TaskView]


class DashboardSummaryView(BaseModel):
    open_tasks: int
    active_projects: int
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
