from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.client_attachment_repository import ClientAttachmentRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import ClientAttachment
from app.infrastructure.db.models import ClientAttachmentModel


class SqlAlchemyClientAttachmentRepository(ClientAttachmentRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: uuid.UUID,
        client_id: uuid.UUID,
        file_id: str,
        filename: str,
        mime_type: str,
    ) -> ClientAttachment:
        row = ClientAttachmentModel(
            user_id=user_id,
            client_id=client_id,
            file_id=file_id,
            filename=filename,
            mime_type=mime_type,
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def list_by_client(self, client_id: uuid.UUID) -> list[ClientAttachment]:
        stmt = (
            select(ClientAttachmentModel)
            .where(ClientAttachmentModel.client_id == client_id)
            .order_by(ClientAttachmentModel.created_at.desc())
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    async def get(self, attachment_id: uuid.UUID) -> ClientAttachment | None:
        row = await self._session.get(ClientAttachmentModel, attachment_id)
        return self._to_entity(row) if row else None

    async def delete(self, attachment_id: uuid.UUID) -> None:
        row = await self._session.get(ClientAttachmentModel, attachment_id)
        if row is None:
            raise NotFoundError(
                "Attachment not found", details={"attachment_id": str(attachment_id)}
            )
        await self._session.delete(row)
        await self._session.flush()

    @staticmethod
    def _to_entity(row: ClientAttachmentModel) -> ClientAttachment:
        return ClientAttachment(
            id=row.id,
            user_id=row.user_id,
            client_id=row.client_id,
            file_id=row.file_id,
            filename=row.filename,
            mime_type=row.mime_type,
            created_at=row.created_at,
        )
