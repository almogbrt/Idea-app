from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.user_repository import UserRepositoryPort
from app.domain.entities import User
from app.infrastructure.db.models import UserModel


class SqlAlchemyUserRepository(UserRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_google_sub(self, google_sub: str) -> User | None:
        row = await self._session.scalar(
            select(UserModel).where(UserModel.google_sub == google_sub)
        )
        return self._to_entity(row) if row else None

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        row = await self._session.get(UserModel, user_id)
        return self._to_entity(row) if row else None

    async def create(self, google_sub: str, email: str, name: str) -> User:
        row = UserModel(google_sub=google_sub, email=email, name=name)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    @staticmethod
    def _to_entity(row: UserModel) -> User:
        return User(
            id=row.id,
            google_sub=row.google_sub,
            email=row.email,
            name=row.name,
            created_at=row.created_at,
        )
