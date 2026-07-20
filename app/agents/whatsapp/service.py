"""WhatsApp service for the `whatsapp` Agent.

Same pattern as `WorkspaceService` (`app/agents/project_management/service.py`):
a long-lived singleton (agents are registered once at process startup), so
it opens a short-lived DB session per call rather than holding a
request-scoped one. Clients are resolved by name, same as the workspace
agent's tools — natural language commands don't carry phone numbers.
"""

from __future__ import annotations

import uuid

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.exceptions import NotFoundError
from app.domain.entities import WhatsAppDirection
from app.infrastructure.db.repositories.client_repository import SqlAlchemyClientRepository
from app.infrastructure.db.repositories.whatsapp_message_repository import (
    SqlAlchemyWhatsAppMessageRepository,
)
from app.infrastructure.whatsapp.client import WhatsAppClient


class WhatsAppService:
    def __init__(
        self, session_factory: async_sessionmaker[AsyncSession], client: WhatsAppClient
    ) -> None:
        self._session_factory = session_factory
        self._client = client

    async def get_conversation(self, user_id: uuid.UUID, client_name: str, limit: int = 50) -> str:
        async with self._session_factory() as session:
            phone_number = await self._resolve_client_phone(session, user_id, client_name)
            messages = await SqlAlchemyWhatsAppMessageRepository(session).list_by_phone_number(
                user_id, phone_number, limit=limit
            )
        if not messages:
            return f"No WhatsApp messages found with {client_name} yet."
        lines = [
            f"[{'them' if m.direction == WhatsAppDirection.INBOUND else 'you'}] {m.content}"
            for m in messages
        ]
        return "\n".join(lines)

    async def send_message(self, user_id: uuid.UUID, client_name: str, message: str) -> None:
        async with self._session_factory() as session:
            phone_number = await self._resolve_client_phone(session, user_id, client_name)
            await self._client.send_text(phone_number, message)
            await SqlAlchemyWhatsAppMessageRepository(session).create(
                user_id, phone_number, WhatsAppDirection.OUTBOUND, message
            )
            await session.commit()

    @staticmethod
    async def _resolve_client_phone(
        session: AsyncSession, user_id: uuid.UUID, client_name: str
    ) -> str:
        clients = await SqlAlchemyClientRepository(session).list_by_user(user_id)
        needle = client_name.strip().lower()
        client = next((c for c in clients if needle in c.name.lower()), None)
        if client is None:
            raise NotFoundError(
                f"No client matching '{client_name}' found", details={"query": client_name}
            )
        if not client.phone:
            raise NotFoundError(
                f"Client '{client.name}' has no phone number on file",
                details={"client_id": str(client.id)},
            )
        return client.phone
