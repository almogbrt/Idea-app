from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.task_repository import TaskRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import Task, TaskImportance, TaskStatus
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
        client_id: uuid.UUID | None = None,
        start_at: datetime | None = None,
    ) -> Task:
        row = TaskModel(
            user_id=user_id,
            title=title,
            project_id=project_id,
            status=TaskStatus.OPEN.value,
            due_at=due_at,
            client_id=client_id,
            start_at=start_at,
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

    async def start_timer(self, task_id: uuid.UUID) -> Task:
        row = await self._session.get(TaskModel, task_id)
        if row is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        row.timer_started_at = datetime.now(UTC)
        row.status = TaskStatus.IN_PROGRESS.value
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def stop_timer(self, task_id: uuid.UUID) -> Task:
        row = await self._session.get(TaskModel, task_id)
        if row is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        row.timer_started_at = None
        row.status = TaskStatus.OPEN.value
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def update_details(
        self,
        task_id: uuid.UUID,
        title: str,
        due_at: datetime | None,
        project_id: uuid.UUID | None,
        client_id: uuid.UUID | None,
        start_at: datetime | None = None,
    ) -> Task:
        row = await self._session.get(TaskModel, task_id)
        if row is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        row.title = title
        row.due_at = due_at
        row.project_id = project_id
        row.client_id = client_id
        row.start_at = start_at
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def delete(self, task_id: uuid.UUID) -> None:
        row = await self._session.get(TaskModel, task_id)
        if row is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        await self._session.delete(row)
        await self._session.flush()

    async def count_open(self, user_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(TaskModel)
            .where(TaskModel.user_id == user_id, TaskModel.status != TaskStatus.DONE.value)
        )
        return (await self._session.execute(stmt)).scalar_one()

    async def set_daily_attributes(
        self,
        task_id: uuid.UUID,
        deliverable: str,
        estimated_minutes: int,
        importance: TaskImportance,
        goal_id: uuid.UUID | None,
    ) -> Task:
        row = await self._session.get(TaskModel, task_id)
        if row is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        row.deliverable = deliverable
        row.estimated_minutes = estimated_minutes
        row.importance = importance.value
        row.goal_id = goal_id
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def set_next_step(self, task_id: uuid.UUID, next_step: str | None) -> Task:
        row = await self._session.get(TaskModel, task_id)
        if row is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        row.next_step = next_step
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

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
            client_id=row.client_id,
            start_at=row.start_at,
            timer_started_at=row.timer_started_at,
            deliverable=row.deliverable,
            estimated_minutes=row.estimated_minutes,
            importance=TaskImportance(row.importance) if row.importance else None,
            goal_id=row.goal_id,
            next_step=row.next_step,
        )
