from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.client_repository import ClientRepositoryPort
from app.domain.entities import Client
from app.infrastructure.db.models import ClientModel


class SqlAlchemyClientRepository(ClientRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: uuid.UUID, name: str) -> Client:
        row = ClientModel(user_id=user_id, name=name)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def list_by_user(self, user_id: uuid.UUID) -> list[Client]:
        stmt = (
            select(ClientModel)
            .where(ClientModel.user_id == user_id)
            .order_by(ClientModel.created_at.desc())
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row: ClientModel) -> Client:
        return Client(id=row.id, user_id=row.user_id, name=row.name, created_at=row.created_at)
