"""Dashboard REST endpoints: Projects/Clients/Tasks + live stats.

These go straight to the use cases, bypassing the LLM tool-call loop
entirely — a dashboard checkbox click shouldn't cost an LLM call. Edith can
still manage the same data through natural language via the
`project_management` Agent (`app/agents/project_management/`); both paths
end up at the same repositories.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends

from app.core.container import RequestScopedServices
from app.core.exceptions import ForbiddenError
from app.domain.entities import (
    Client,
    ClientDetail,
    Notification,
    Project,
    ProjectSummary,
    Task,
    User,
)
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from app.interfaces.api.schemas.workspace import (
    ActivityItemView,
    ClientDetailView,
    ClientView,
    CreateClientRequest,
    CreateProjectRequest,
    CreateTaskRequest,
    DashboardSummaryView,
    NotificationView,
    ProjectView,
    TaskView,
    UpdateClientRequest,
    UpdateProjectStatusRequest,
    UpdateTaskDueAtRequest,
    UpdateTaskStatusRequest,
)

router = APIRouter(tags=["workspace"])


def _ensure_client_owned_by(client: Client, user: User) -> None:
    if client.user_id != user.id:
        raise ForbiddenError("This client does not belong to you.")


def _ensure_project_owned_by(project: Project, user: User) -> None:
    if project.user_id != user.id:
        raise ForbiddenError("This project does not belong to you.")


def _ensure_task_owned_by(task: Task, user: User) -> None:
    if task.user_id != user.id:
        raise ForbiddenError("This task does not belong to you.")


@router.get("/dashboard/summary", response_model=DashboardSummaryView)
async def dashboard_summary(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> DashboardSummaryView:
    summary = await scope.dashboard_summary.execute(user.id)
    return DashboardSummaryView(
        open_tasks=summary.open_tasks,
        active_projects=summary.active_projects,
        unread_emails=summary.unread_emails,
        meetings_today=summary.meetings_today,
    )


@router.get("/dashboard/activity", response_model=list[ActivityItemView])
async def dashboard_activity(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> list[ActivityItemView]:
    executions = await scope.list_activity.list_recent(user.id, limit=10)
    return [
        ActivityItemView(
            id=e.id,
            agent_name=e.agent_name,
            tool_name=e.tool_name,
            status=e.status.value,
            created_at=e.created_at,
        )
        for e in executions
    ]


def _client_view(client: Client) -> ClientView:
    return ClientView(
        id=client.id,
        name=client.name,
        created_at=client.created_at,
        email=client.email,
        phone=client.phone,
        notes=client.notes,
        next_follow_up_at=client.next_follow_up_at,
    )


@router.get("/clients", response_model=list[ClientView])
async def list_clients(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> list[ClientView]:
    clients = await scope.manage_clients.list_all(user.id)
    return [_client_view(c) for c in clients]


@router.post("/clients", response_model=ClientView)
async def create_client(
    body: CreateClientRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> ClientView:
    client = await scope.manage_clients.create(user.id, body.name)
    return _client_view(client)


@router.get("/clients/{client_id}", response_model=ClientDetailView)
async def get_client(
    client_id: uuid.UUID,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> ClientDetailView:
    client = await scope.manage_clients.get_or_raise(client_id)
    _ensure_client_owned_by(client, user)
    detail: ClientDetail = await scope.manage_clients.get_detail(user.id, client_id)
    return ClientDetailView(
        client=_client_view(detail.client),
        projects=[_project_view(s) for s in detail.projects],
        tasks=[_task_view(t) for t in detail.tasks],
    )


@router.patch("/clients/{client_id}", response_model=ClientView)
async def update_client(
    client_id: uuid.UUID,
    body: UpdateClientRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> ClientView:
    existing = await scope.manage_clients.get_or_raise(client_id)
    _ensure_client_owned_by(existing, user)
    updated = await scope.manage_clients.update(
        client_id,
        name=body.name,
        email=body.email,
        phone=body.phone,
        notes=body.notes,
        next_follow_up_at=body.next_follow_up_at,
    )
    return _client_view(updated)


def _project_view(summary: ProjectSummary) -> ProjectView:
    return ProjectView(
        id=summary.project.id,
        name=summary.project.name,
        status=summary.project.status,
        client_id=summary.project.client_id,
        client_name=summary.client_name,
        last_task_title=summary.last_task_title,
        created_at=summary.project.created_at,
        updated_at=summary.project.updated_at,
    )


@router.get("/projects", response_model=list[ProjectView])
async def list_projects(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> list[ProjectView]:
    summaries = await scope.manage_projects.list_all(user.id)
    return [_project_view(s) for s in summaries]


@router.post("/projects", response_model=ProjectView)
async def create_project(
    body: CreateProjectRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> ProjectView:
    project = await scope.manage_projects.create(user.id, body.name, body.client_id)
    summary = await scope.manage_projects.get_summary_or_raise(project.id)
    return _project_view(summary)


@router.patch("/projects/{project_id}/status", response_model=ProjectView)
async def update_project_status(
    project_id: uuid.UUID,
    body: UpdateProjectStatusRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> ProjectView:
    existing = await scope.manage_projects.get_or_raise(project_id)
    _ensure_project_owned_by(existing, user)
    await scope.manage_projects.update_status(project_id, body.status)
    summary = await scope.manage_projects.get_summary_or_raise(project_id)
    return _project_view(summary)


@router.get("/tasks", response_model=list[TaskView])
async def list_tasks(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> list[TaskView]:
    tasks = await scope.manage_tasks.list_all(user.id)
    return [_task_view(t) for t in tasks]


def _task_view(task: Task) -> TaskView:
    return TaskView(
        id=task.id,
        title=task.title,
        status=task.status,
        project_id=task.project_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
        due_at=task.due_at,
    )


@router.post("/tasks", response_model=TaskView)
async def create_task(
    body: CreateTaskRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> TaskView:
    task = await scope.manage_tasks.create(user.id, body.title, body.project_id, body.due_at)
    return _task_view(task)


@router.patch("/tasks/{task_id}/status", response_model=TaskView)
async def update_task_status(
    task_id: uuid.UUID,
    body: UpdateTaskStatusRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> TaskView:
    existing = await scope.manage_tasks.get_or_raise(task_id)
    _ensure_task_owned_by(existing, user)
    updated = await scope.manage_tasks.update_status(task_id, body.status)
    return _task_view(updated)


@router.patch("/tasks/{task_id}/due-date", response_model=TaskView)
async def update_task_due_at(
    task_id: uuid.UUID,
    body: UpdateTaskDueAtRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> TaskView:
    existing = await scope.manage_tasks.get_or_raise(task_id)
    _ensure_task_owned_by(existing, user)
    updated = await scope.manage_tasks.set_due_at(task_id, body.due_at)
    return _task_view(updated)


def _notification_view(notification: Notification) -> NotificationView:
    return NotificationView(
        id=notification.id,
        kind=notification.kind,
        related_id=notification.related_id,
        title=notification.title,
        body=notification.body,
        created_at=notification.created_at,
        read_at=notification.read_at,
    )


@router.get("/notifications", response_model=list[NotificationView])
async def list_notifications(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> list[NotificationView]:
    notifications = await scope.manage_notifications.list_unread(user.id)
    return [_notification_view(n) for n in notifications]


def _ensure_notification_owned_by(notification: Notification, user: User) -> None:
    if notification.user_id != user.id:
        raise ForbiddenError("This notification does not belong to you.")


@router.patch("/notifications/{notification_id}/read", response_model=NotificationView)
async def mark_notification_read(
    notification_id: uuid.UUID,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> NotificationView:
    existing = await scope.manage_notifications.get_or_raise(notification_id)
    _ensure_notification_owned_by(existing, user)
    notification = await scope.manage_notifications.mark_read(notification_id)
    return _notification_view(notification)


@router.post("/notifications/read-all", status_code=204)
async def mark_all_notifications_read(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> None:
    await scope.manage_notifications.mark_all_read(user.id)
