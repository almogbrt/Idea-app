"""Workspace (Client/Project/Task) service for the `project_management` Agent.

Follows the same pattern as `GoogleApiClientFactory`
(`app/infrastructure/google/api_client_factory.py`): this is a long-lived
singleton shared by the agent's tools (agents are registered once at process
startup), so it must not hold a request-scoped `AsyncSession`. It opens a
short-lived session per call instead.

Entities are addressed by name/title here, not UUID — natural language
commands don't carry database IDs, so each mutation resolves its target by a
case-insensitive match against the user's own records.
"""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.exceptions import NotFoundError
from app.domain.entities import Client, Project, ProjectStatus, ProjectSummary, Task, TaskStatus
from app.infrastructure.db.repositories.client_repository import SqlAlchemyClientRepository
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.task_repository import SqlAlchemyTaskRepository


class WorkspaceService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def create_client(self, user_id: uuid.UUID, name: str) -> Client:
        async with self._session_factory() as session:
            client = await self._find_client(session, user_id, name)
            if client is not None:
                return client
            client = await SqlAlchemyClientRepository(session).create(user_id, name)
            await session.commit()
            return client

    async def create_project(
        self, user_id: uuid.UUID, name: str, client_name: str | None = None
    ) -> Project:
        async with self._session_factory() as session:
            client_id = None
            if client_name:
                client = await self._find_client(session, user_id, client_name)
                if client is None:
                    client = await SqlAlchemyClientRepository(session).create(
                        user_id, client_name
                    )
                client_id = client.id
            project = await SqlAlchemyProjectRepository(session).create(
                user_id, name, client_id=client_id
            )
            await session.commit()
            return project

    async def update_project_status(
        self, user_id: uuid.UUID, project_name: str, status: ProjectStatus
    ) -> Project:
        async with self._session_factory() as session:
            project = await self._find_project(session, user_id, project_name)
            updated = await SqlAlchemyProjectRepository(session).update_status(
                project.id, status
            )
            await session.commit()
            return updated

    async def list_projects(self, user_id: uuid.UUID) -> list[ProjectSummary]:
        async with self._session_factory() as session:
            return await SqlAlchemyProjectRepository(session).list_by_user(user_id)

    async def create_task(
        self, user_id: uuid.UUID, title: str, project_name: str | None = None
    ) -> Task:
        async with self._session_factory() as session:
            project_id = None
            if project_name:
                project = await self._find_project(session, user_id, project_name)
                project_id = project.id
            task = await SqlAlchemyTaskRepository(session).create(
                user_id, title, project_id=project_id
            )
            await session.commit()
            return task

    async def update_task_status(
        self, user_id: uuid.UUID, task_title: str, status: TaskStatus
    ) -> Task:
        async with self._session_factory() as session:
            task = await self._find_task(session, user_id, task_title)
            updated = await SqlAlchemyTaskRepository(session).update_status(task.id, status)
            await session.commit()
            return updated

    async def list_tasks(self, user_id: uuid.UUID) -> list[Task]:
        async with self._session_factory() as session:
            return await SqlAlchemyTaskRepository(session).list_by_user(user_id)

    @staticmethod
    async def _find_client(session: AsyncSession, user_id: uuid.UUID, name: str) -> Client | None:
        clients = await SqlAlchemyClientRepository(session).list_by_user(user_id)
        needle = name.strip().lower()
        return next((c for c in clients if needle in c.name.lower()), None)

    @staticmethod
    async def _find_project(session: AsyncSession, user_id: uuid.UUID, name: str) -> Project:
        summaries = await SqlAlchemyProjectRepository(session).list_by_user(user_id)
        needle = name.strip().lower()
        for summary in summaries:
            if needle in summary.project.name.lower():
                return summary.project
        raise NotFoundError(f"No project matching '{name}' found", details={"query": name})

    @staticmethod
    async def _find_task(session: AsyncSession, user_id: uuid.UUID, title: str) -> Task:
        tasks = await SqlAlchemyTaskRepository(session).list_by_user(user_id)
        needle = title.strip().lower()
        for task in tasks:
            if needle in task.title.lower():
                return task
        raise NotFoundError(f"No task matching '{title}' found", details={"query": title})
