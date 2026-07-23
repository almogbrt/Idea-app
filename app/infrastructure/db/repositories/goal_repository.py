from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.goal_repository import GoalRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import Goal
from app.infrastructure.db.models import GoalModel


class SqlAlchemyGoalRepository(GoalRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: uuid.UUID, name: str) -> Goal:
        row = GoalModel(user_id=user_id, name=name)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def list_by_user(self, user_id: uuid.UUID) -> list[Goal]:
        stmt = (
            select(GoalModel)
            .where(GoalModel.user_id == user_id)
            .order_by(GoalModel.created_at.desc())
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    async def get(self, goal_id: uuid.UUID) -> Goal | None:
        row = await self._session.get(GoalModel, goal_id)
        return self._to_entity(row) if row else None

    async def update(self, goal_id: uuid.UUID, name: str) -> Goal:
        row = await self._session.get(GoalModel, goal_id)
        if row is None:
            raise NotFoundError("Goal not found", details={"goal_id": str(goal_id)})
        row.name = name
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def delete(self, goal_id: uuid.UUID) -> None:
        row = await self._session.get(GoalModel, goal_id)
        if row is None:
            raise NotFoundError("Goal not found", details={"goal_id": str(goal_id)})
        await self._session.delete(row)
        await self._session.flush()

    @staticmethod
    def _to_entity(row: GoalModel) -> Goal:
        return Goal(
            id=row.id,
            user_id=row.user_id,
            name=row.name,
            created_at=row.created_at,
        )
