from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.task_repository import TaskRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import Task, TaskStatus
from app.infrastructure.db.models import TaskModel


class SqlAlchemyTaskRepository(TaskRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: uuid.UUID,
        title: str,
        project_id: uuid.UUID | None = None,
        due_at: datetime | None = None,
    ) -> Task:
        row = TaskModel(
            user_id=user_id,
            title=title,
            project_id=project_id,
            status=TaskStatus.OPEN.value,
            due_at=due_at,
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def list_by_user(self, user_id: uuid.UUID) -> list[Task]:
        stmt = (
            select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .order_by(TaskModel.updated_at.desc())
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    async def get(self, task_id: uuid.UUID) -> Task | None:
        row = await self._session.get(TaskModel, task_id)
        return self._to_entity(row) if row else None

    async def update_status(self, task_id: uuid.UUID, status: TaskStatus) -> Task:
        row = await self._session.get(TaskModel, task_id)
        if row is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        row.status = status.value
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def set_due_at(self, task_id: uuid.UUID, due_at: datetime | None) -> Task:
        row = await self._session.get(TaskModel, task_id)
        if row is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        row.due_at = due_at
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def count_open(self, user_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(TaskModel)
            .where(TaskModel.user_id == user_id, TaskModel.status != TaskStatus.DONE.value)
        )
        return (await self._session.execute(stmt)).scalar_one()

    @staticmethod
    def _to_entity(row: TaskModel) -> Task:
        return Task(
            id=row.id,
            user_id=row.user_id,
            project_id=row.project_id,
            title=row.title,
            status=TaskStatus(row.status),
            created_at=row.created_at,
            updated_at=row.updated_at,
            due_at=row.due_at,
        )
