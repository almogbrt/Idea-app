from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.whatsapp_message_repository import WhatsAppMessageRepositoryPort
from app.domain.entities import WhatsAppDirection, WhatsAppMessage
from app.infrastructure.db.models import WhatsAppMessageModel


class SqlAlchemyWhatsAppMessageRepository(WhatsAppMessageRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: uuid.UUID,
        phone_number: str,
        direction: WhatsAppDirection,
        content: str,
    ) -> WhatsAppMessage:
        row = WhatsAppMessageModel(
            user_id=user_id,
            phone_number=phone_number,
            direction=direction.value,
            content=content,
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def list_by_phone_number(
        self, user_id: uuid.UUID, phone_number: str, limit: int = 50
    ) -> list[WhatsAppMessage]:
        stmt = (
            select(WhatsAppMessageModel)
            .where(
                WhatsAppMessageModel.user_id == user_id,
                WhatsAppMessageModel.phone_number == phone_number,
            )
            .order_by(WhatsAppMessageModel.sequence.desc())
            .limit(limit)
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in reversed(rows)]

    @staticmethod
    def _to_entity(row: WhatsAppMessageModel) -> WhatsAppMessage:
        return WhatsAppMessage(
            id=row.id,
            user_id=row.user_id,
            phone_number=row.phone_number,
            direction=WhatsAppDirection(row.direction),
            content=row.content,
            created_at=row.created_at,
        )
