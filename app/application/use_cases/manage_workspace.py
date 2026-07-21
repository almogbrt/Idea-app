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
from app.application.ports.client_attachment_repository import ClientAttachmentRepositoryPort
from app.application.ports.client_logo_storage import ClientLogoStoragePort
from app.application.ports.client_repository import ClientRepositoryPort
from app.application.ports.inbox import InboxPort
from app.application.ports.project_repository import ProjectRepositoryPort
from app.application.ports.schedule import SchedulePort
from app.application.ports.task_repository import TaskRepositoryPort
from app.application.ports.thought_repository import ThoughtRepositoryPort
from app.core.exceptions import AuthError, ExternalServiceError, NotFoundError, ValidationError
from app.core.logging import get_logger
from app.domain.entities import (
    AgentExecution,
    Client,
    ClientAttachment,
    ClientDetail,
    Project,
    ProjectSummary,
    ProjectType,
    Task,
    TaskStatus,
    Thought,
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
        logo_storage: ClientLogoStoragePort,
        attachment_repository: ClientAttachmentRepositoryPort,
    ) -> None:
        self._clients = client_repository
        self._projects = project_repository
        self._tasks = task_repository
        self._logo_storage = logo_storage
        self._attachments = attachment_repository

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
    ) -> Client:
        return await self._clients.update(
            client_id,
            name=name,
            email=email,
            phone=phone,
            notes=notes,
        )

    async def delete(self, client_id: uuid.UUID) -> None:
        await self._clients.delete(client_id)

    async def upload_logo(
        self,
        user_id: uuid.UUID,
        client_id: uuid.UUID,
        filename: str,
        content: bytes,
        mime_type: str,
    ) -> Client:
        await self.get_or_raise(client_id)
        file_id = await self._logo_storage.upload(user_id, filename, content, mime_type)
        return await self._clients.update(client_id, logo_file_id=file_id)

    async def get_logo(self, user_id: uuid.UUID, client_id: uuid.UUID) -> tuple[bytes, str]:
        client = await self.get_or_raise(client_id)
        if client.logo_file_id is None:
            raise NotFoundError("Client has no logo", details={"client_id": str(client_id)})
        return await self._logo_storage.download(user_id, client.logo_file_id)

    async def get_detail(self, user_id: uuid.UUID, client_id: uuid.UUID) -> ClientDetail:
        """The "full history" view: the client plus every project, task, and
        attachment linked to it, however many hops that takes today (task ->
        project -> client) since neither repository can filter by client_id
        directly."""
        client = await self.get_or_raise(client_id)

        all_projects = await self._projects.list_by_user(user_id)
        client_projects = [
            summary for summary in all_projects if summary.project.client_id == client_id
        ]
        project_ids = {summary.project.id for summary in client_projects}

        all_tasks = await self._tasks.list_by_user(user_id)
        client_tasks = [
            task
            for task in all_tasks
            if task.project_id in project_ids or task.client_id == client_id
        ]

        attachments = await self._attachments.list_by_client(client_id)

        return ClientDetail(
            client=client, projects=client_projects, tasks=client_tasks, attachments=attachments
        )

    async def upload_attachment(
        self,
        user_id: uuid.UUID,
        client_id: uuid.UUID,
        filename: str,
        content: bytes,
        mime_type: str,
    ) -> ClientAttachment:
        await self.get_or_raise(client_id)
        file_id = await self._logo_storage.upload(user_id, filename, content, mime_type)
        return await self._attachments.create(user_id, client_id, file_id, filename, mime_type)

    async def download_attachment(
        self, user_id: uuid.UUID, client_id: uuid.UUID, attachment_id: uuid.UUID
    ) -> tuple[bytes, str, str]:
        attachment = await self._get_attachment_or_raise(client_id, attachment_id)
        content, mime_type = await self._logo_storage.download(user_id, attachment.file_id)
        return content, mime_type, attachment.filename

    async def delete_attachment(
        self, user_id: uuid.UUID, client_id: uuid.UUID, attachment_id: uuid.UUID
    ) -> None:
        attachment = await self._get_attachment_or_raise(client_id, attachment_id)
        await self._logo_storage.delete(user_id, attachment.file_id)
        await self._attachments.delete(attachment_id)

    async def _get_attachment_or_raise(
        self, client_id: uuid.UUID, attachment_id: uuid.UUID
    ) -> ClientAttachment:
        attachment = await self._attachments.get(attachment_id)
        if attachment is None or attachment.client_id != client_id:
            raise NotFoundError(
                "Attachment not found", details={"attachment_id": str(attachment_id)}
            )
        return attachment


class ManageProjectsUseCase:
    def __init__(self, project_repository: ProjectRepositoryPort) -> None:
        self._projects = project_repository

    async def create(
        self,
        user_id: uuid.UUID,
        name: str,
        client_id: uuid.UUID | None = None,
        type: ProjectType | None = None,
    ) -> Project:
        if client_id is None:
            raise ValidationError("A new project needs a client.")
        if type is None:
            raise ValidationError("A new project needs a type.")
        return await self._projects.create(user_id, name, client_id, type)

    async def list_all(self, user_id: uuid.UUID) -> list[ProjectSummary]:
        return await self._projects.list_by_user(user_id)

    async def update_type(self, project_id: uuid.UUID, type: ProjectType) -> Project:
        return await self._projects.update_type(project_id, type)

    async def assign_client(self, project_id: uuid.UUID, client_id: uuid.UUID) -> Project:
        return await self._projects.assign_client(project_id, client_id)

    async def delete(self, project_id: uuid.UUID) -> None:
        await self._projects.delete(project_id)

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
        client_id: uuid.UUID | None = None,
        start_at: datetime | None = None,
    ) -> Task:
        if start_at is None or due_at is None:
            raise ValidationError(
                "A new task needs both a start time and an end time.",
                details={
                    "start_at": start_at.isoformat() if start_at else None,
                    "due_at": due_at.isoformat() if due_at else None,
                },
            )
        return await self._tasks.create(user_id, title, project_id, due_at, client_id, start_at)

    async def list_all(self, user_id: uuid.UUID) -> list[Task]:
        return await self._tasks.list_by_user(user_id)

    async def update_status(self, task_id: uuid.UUID, status: TaskStatus) -> Task:
        return await self._tasks.update_status(task_id, status)

    async def set_due_at(self, task_id: uuid.UUID, due_at: datetime | None) -> Task:
        return await self._tasks.set_due_at(task_id, due_at)

    async def update_details(
        self,
        task_id: uuid.UUID,
        title: str,
        due_at: datetime | None,
        project_id: uuid.UUID | None,
        client_id: uuid.UUID | None,
        start_at: datetime | None = None,
    ) -> Task:
        """A full-form save — unlike `create`, editing an existing task does
        not force adding a start/end time retroactively if it never had one."""
        return await self._tasks.update_details(
            task_id, title, due_at, project_id, client_id, start_at
        )

    async def delete(self, task_id: uuid.UUID) -> None:
        await self._tasks.delete(task_id)

    async def get_or_raise(self, task_id: uuid.UUID) -> Task:
        task = await self._tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        return task


class ManageThoughtsUseCase:
    def __init__(self, thought_repository: ThoughtRepositoryPort) -> None:
        self._thoughts = thought_repository

    async def create(self, user_id: uuid.UUID, content: str) -> Thought:
        stripped = content.strip()
        if not stripped:
            raise ValidationError("A thought needs some content.")
        return await self._thoughts.create(user_id, stripped)

    async def list_all(self, user_id: uuid.UUID) -> list[Thought]:
        return await self._thoughts.list_by_user(user_id)

    async def get_or_raise(self, thought_id: uuid.UUID) -> Thought:
        thought = await self._thoughts.get(thought_id)
        if thought is None:
            raise NotFoundError("Thought not found", details={"thought_id": str(thought_id)})
        return thought

    async def delete(self, thought_id: uuid.UUID) -> None:
        await self._thoughts.delete(thought_id)


@dataclass(frozen=True, slots=True)
class DashboardSummary:
    open_tasks: int
    active_projects: int
    total_clients: int
    unread_emails: int | None
    """None means "unavailable" (Google not linked yet, or the call failed) —
    the UI should render this as a dash, not a zero."""
    meetings_today: int | None


class DashboardSummaryUseCase:
    def __init__(
        self,
        project_repository: ProjectRepositoryPort,
        task_repository: TaskRepositoryPort,
        client_repository: ClientRepositoryPort,
        inbox: InboxPort,
        schedule: SchedulePort,
    ) -> None:
        self._projects = project_repository
        self._tasks = task_repository
        self._clients = client_repository
        self._inbox = inbox
        self._schedule = schedule

    async def execute(self, user_id: uuid.UUID) -> DashboardSummary:
        open_tasks = await self._tasks.count_open(user_id)
        active_projects = await self._projects.count_active(user_id)
        total_clients = await self._clients.count(user_id)
        unread_emails = await self._safe_call(self._inbox.count_unread, user_id)
        meetings_today = await self._safe_call(self._schedule.count_meetings_today, user_id)

        return DashboardSummary(
            open_tasks=open_tasks,
            active_projects=active_projects,
            total_clients=total_clients,
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
