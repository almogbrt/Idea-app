from __future__ import annotations

import uuid

from app.application.ports.whatsapp_message_repository import WhatsAppMessageRepositoryPort
from app.domain.entities import WhatsAppDirection, WhatsAppMessage


class ManageWhatsAppMessagesUseCase:
    """Thin wrapper used by the inbound webhook to log client-side messages
    (the owner's own messages are routed to the Orchestrator instead, see
    `app/interfaces/api/v1/whatsapp_webhook.py`)."""

    def __init__(self, whatsapp_message_repository: WhatsAppMessageRepositoryPort) -> None:
        self._messages = whatsapp_message_repository

    async def log_inbound(
        self, user_id: uuid.UUID, phone_number: str, content: str
    ) -> WhatsAppMessage:
        return await self._messages.create(
            user_id, phone_number, WhatsAppDirection.INBOUND, content
        )
