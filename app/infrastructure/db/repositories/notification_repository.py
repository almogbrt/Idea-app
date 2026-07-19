from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.notification_repository import NotificationRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import Notification, NotificationKind
from app.infrastructure.db.models import NotificationModel


class SqlAlchemyNotificationRepository(NotificationRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: uuid.UUID,
        kind: NotificationKind,
        related_id: uuid.UUID,
        title: str,
        body: str,
    ) -> Notification:
        row = NotificationModel(
            user_id=user_id, kind=kind.value, related_id=related_id, title=title, body=body
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def exists(
        self, user_id: uuid.UUID, kind: NotificationKind, related_id: uuid.UUID
    ) -> bool:
        stmt = select(
            exists().where(
                NotificationModel.user_id == user_id,
                NotificationModel.kind == kind.value,
                NotificationModel.related_id == related_id,
            )
        )
        return bool((await self._session.execute(stmt)).scalar_one())

    async def get(self, notification_id: uuid.UUID) -> Notification | None:
        row = await self._session.get(NotificationModel, notification_id)
        return self._to_entity(row) if row else None

    async def list_unread(self, user_id: uuid.UUID) -> list[Notification]:
        stmt = (
            select(NotificationModel)
            .where(NotificationModel.user_id == user_id, NotificationModel.read_at.is_(None))
            .order_by(NotificationModel.created_at.desc())
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    async def mark_read(self, notification_id: uuid.UUID) -> Notification:
        row = await self._session.get(NotificationModel, notification_id)
        if row is None:
            raise NotFoundError(
                "Notification not found", details={"notification_id": str(notification_id)}
            )
        row.read_at = datetime.now(UTC)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def mark_all_read(self, user_id: uuid.UUID) -> None:
        stmt = select(NotificationModel).where(
            NotificationModel.user_id == user_id, NotificationModel.read_at.is_(None)
        )
        rows = (await self._session.scalars(stmt)).all()
        now = datetime.now(UTC)
        for row in rows:
            row.read_at = now
        await self._session.flush()

    @staticmethod
    def _to_entity(row: NotificationModel) -> Notification:
        return Notification(
            id=row.id,
            user_id=row.user_id,
            kind=NotificationKind(row.kind),
            related_id=row.related_id,
            title=row.title,
            body=row.body,
            created_at=row.created_at,
            read_at=row.read_at,
        )
