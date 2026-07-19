"""Use cases behind the Projects/Clients/Tasks dashboard.

Thin CRUD wrappers, same shape as `ManageConversationUseCase`, plus
`DashboardSummaryUseCase` which aggregates local (always-available) counts
with live Google data that degrades gracefully if the account isn't linked
yet or a call fails.
"""

from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import datetime

from app.application.ports.agent_execution_repository import AgentExecutionRepositoryPort
from app.application.ports.client_repository import ClientRepositoryPort
from app.application.ports.inbox import InboxPort
from app.application.ports.project_repository import ProjectRepositoryPort
from app.application.ports.schedule import SchedulePort
from app.application.ports.task_repository import TaskRepositoryPort
from app.core.exceptions import AuthError, ExternalServiceError, NotFoundError
from app.core.logging import get_logger
from app.domain.entities import (
    AgentExecution,
    Client,
    ClientDetail,
    Project,
    ProjectStatus,
    ProjectSummary,
    Task,
    TaskStatus,
)

logger = get_logger(__name__)


class ListActivityUseCase:
    def __init__(self, agent_execution_repository: AgentExecutionRepositoryPort) -> None:
        self._executions = agent_execution_repository

    async def list_recent(self, user_id: uuid.UUID, limit: int = 10) -> list[AgentExecution]:
        return await self._executions.list_recent(user_id, limit)


class ManageClientsUseCase:
    def __init__(
        self,
        client_repository: ClientRepositoryPort,
        project_repository: ProjectRepositoryPort,
        task_repository: TaskRepositoryPort,
    ) -> None:
        self._clients = client_repository
        self._projects = project_repository
        self._tasks = task_repository

    async def create(self, user_id: uuid.UUID, name: str) -> Client:
        return await self._clients.create(user_id, name)

    async def list_all(self, user_id: uuid.UUID) -> list[Client]:
        return await self._clients.list_by_user(user_id)

    async def get_or_raise(self, client_id: uuid.UUID) -> Client:
        client = await self._clients.get(client_id)
        if client is None:
            raise NotFoundError("Client not found", details={"client_id": str(client_id)})
        return client

    async def update(
        self,
        client_id: uuid.UUID,
        *,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        notes: str | None = None,
        next_follow_up_at: datetime | None = None,
    ) -> Client:
        return await self._clients.update(
            client_id,
            name=name,
            email=email,
            phone=phone,
            notes=notes,
            next_follow_up_at=next_follow_up_at,
        )

    async def get_detail(self, user_id: uuid.UUID, client_id: uuid.UUID) -> ClientDetail:
        """The "full history" view: the client plus every project and task
        linked to it, however many hops that takes today (task -> project ->
        client) since neither repository can filter by client_id directly."""
        client = await self.get_or_raise(client_id)

        all_projects = await self._projects.list_by_user(user_id)
        client_projects = [
            summary for summary in all_projects if summary.project.client_id == client_id
        ]
        project_ids = {summary.project.id for summary in client_projects}

        all_tasks = await self._tasks.list_by_user(user_id)
        client_tasks = [task for task in all_tasks if task.project_id in project_ids]

        return ClientDetail(client=client, projects=client_projects, tasks=client_tasks)


class ManageProjectsUseCase:
    def __init__(self, project_repository: ProjectRepositoryPort) -> None:
        self._projects = project_repository

    async def create(
        self, user_id: uuid.UUID, name: str, client_id: uuid.UUID | None = None
    ) -> Project:
        return await self._projects.create(user_id, name, client_id)

    async def list_all(self, user_id: uuid.UUID) -> list[ProjectSummary]:
        return await self._projects.list_by_user(user_id)

    async def update_status(self, project_id: uuid.UUID, status: ProjectStatus) -> Project:
        return await self._projects.update_status(project_id, status)

    async def get_or_raise(self, project_id: uuid.UUID) -> Project:
        project = await self._projects.get(project_id)
        if project is None:
            raise NotFoundError("Project not found", details={"project_id": str(project_id)})
        return project

    async def get_summary_or_raise(self, project_id: uuid.UUID) -> ProjectSummary:
        summary = await self._projects.get_summary(project_id)
        if summary is None:
            raise NotFoundError("Project not found", details={"project_id": str(project_id)})
        return summary


class ManageTasksUseCase:
    def __init__(self, task_repository: TaskRepositoryPort) -> None:
        self._tasks = task_repository

    async def create(
        self,
        user_id: uuid.UUID,
        title: str,
        project_id: uuid.UUID | None = None,
        due_at: datetime | None = None,
    ) -> Task:
        return await self._tasks.create(user_id, title, project_id, due_at)

    async def list_all(self, user_id: uuid.UUID) -> list[Task]:
        return await self._tasks.list_by_user(user_id)

    async def update_status(self, task_id: uuid.UUID, status: TaskStatus) -> Task:
        return await self._tasks.update_status(task_id, status)

    async def set_due_at(self, task_id: uuid.UUID, due_at: datetime | None) -> Task:
        return await self._tasks.set_due_at(task_id, due_at)

    async def get_or_raise(self, task_id: uuid.UUID) -> Task:
        task = await self._tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        return task


@dataclass(frozen=True, slots=True)
class DashboardSummary:
    open_tasks: int
    active_projects: int
    unread_emails: int | None
    """None means "unavailable" (Google not linked yet, or the call failed) —
    the UI should render this as a dash, not a zero."""
    meetings_today: int | None


class DashboardSummaryUseCase:
    def __init__(
        self,
        project_repository: ProjectRepositoryPort,
        task_repository: TaskRepositoryPort,
        inbox: InboxPort,
        schedule: SchedulePort,
    ) -> None:
        self._projects = project_repository
        self._tasks = task_repository
        self._inbox = inbox
        self._schedule = schedule

    async def execute(self, user_id: uuid.UUID) -> DashboardSummary:
        open_tasks = await self._tasks.count_open(user_id)
        active_projects = await self._projects.count_active(user_id)
        unread_emails = await self._safe_call(self._inbox.count_unread, user_id)
        meetings_today = await self._safe_call(self._schedule.count_meetings_today, user_id)

        return DashboardSummary(
            open_tasks=open_tasks,
            active_projects=active_projects,
            unread_emails=unread_emails,
            meetings_today=meetings_today,
        )

    @staticmethod
    async def _safe_call(
        fn: Callable[[uuid.UUID], Awaitable[int]], user_id: uuid.UUID
    ) -> int | None:
        try:
            return await fn(user_id)
        except (AuthError, ExternalServiceError) as exc:
            logger.info("dashboard_live_stat_unavailable", error=str(exc))
            return None
