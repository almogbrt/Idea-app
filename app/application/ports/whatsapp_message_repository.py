from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import WhatsAppDirection, WhatsAppMessage


class WhatsAppMessageRepositoryPort(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: uuid.UUID,
        phone_number: str,
        direction: WhatsAppDirection,
        content: str,
    ) -> WhatsAppMessage:
        raise NotImplementedError

    @abstractmethod
    async def list_by_phone_number(
        self, user_id: uuid.UUID, phone_number: str, limit: int = 50
    ) -> list[WhatsAppMessage]:
        """Returns messages ordered oldest-first, most recent `limit` only."""
        raise NotImplementedError
