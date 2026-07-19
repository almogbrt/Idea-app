from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.entities import Client


class ClientRepositoryPort(ABC):
    @abstractmethod
    async def create(self, user_id: uuid.UUID, name: str) -> Client:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: uuid.UUID) -> list[Client]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, client_id: uuid.UUID) -> Client | None:
        raise NotImplementedError

    @abstractmethod
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
        """Only fields explicitly passed are changed; omitted (`None`) fields
        keep their current stored value."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, client_id: uuid.UUID) -> None:
        raise NotImplementedError
