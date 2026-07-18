from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import Client


class ClientRepositoryPort(ABC):
    @abstractmethod
    async def create(self, user_id: uuid.UUID, name: str) -> Client:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: uuid.UUID) -> list[Client]:
        raise NotImplementedError
