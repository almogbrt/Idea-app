from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.client_repository import ClientRepositoryPort
from app.core.exceptions import NotFoundError
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

    async def get(self, client_id: uuid.UUID) -> Client | None:
        row = await self._session.get(ClientModel, client_id)
        return self._to_entity(row) if row else None

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
        row = await self._session.get(ClientModel, client_id)
        if row is None:
            raise NotFoundError("Client not found", details={"client_id": str(client_id)})
        if name is not None:
            row.name = name
        if email is not None:
            row.email = email
        if phone is not None:
            row.phone = phone
        if notes is not None:
            row.notes = notes
        if next_follow_up_at is not None:
            row.next_follow_up_at = next_follow_up_at
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    @staticmethod
    def _to_entity(row: ClientModel) -> Client:
        return Client(
            id=row.id,
            user_id=row.user_id,
            name=row.name,
            created_at=row.created_at,
            email=row.email,
            phone=row.phone,
            notes=row.notes,
            next_follow_up_at=row.next_follow_up_at,
        )
