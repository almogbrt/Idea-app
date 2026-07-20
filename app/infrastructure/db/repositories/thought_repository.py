from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.thought_repository import ThoughtRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import Thought
from app.infrastructure.db.models import ThoughtModel


class SqlAlchemyThoughtRepository(ThoughtRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: uuid.UUID, content: str) -> Thought:
        row = ThoughtModel(user_id=user_id, content=content)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def list_by_user(self, user_id: uuid.UUID) -> list[Thought]:
        stmt = (
            select(ThoughtModel)
            .where(ThoughtModel.user_id == user_id)
            .order_by(ThoughtModel.created_at.desc())
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    async def get(self, thought_id: uuid.UUID) -> Thought | None:
        row = await self._session.get(ThoughtModel, thought_id)
        return self._to_entity(row) if row else None

    async def delete(self, thought_id: uuid.UUID) -> None:
        row = await self._session.get(ThoughtModel, thought_id)
        if row is None:
            raise NotFoundError("Thought not found", details={"thought_id": str(thought_id)})
        await self._session.delete(row)
        await self._session.flush()

    @staticmethod
    def _to_entity(row: ThoughtModel) -> Thought:
        return Thought(
            id=row.id,
            user_id=row.user_id,
            content=row.content,
            created_at=row.created_at,
        )
