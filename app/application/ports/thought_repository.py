from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import Thought


class ThoughtRepositoryPort(ABC):
    @abstractmethod
    async def create(self, user_id: uuid.UUID, content: str) -> Thought:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: uuid.UUID) -> list[Thought]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, thought_id: uuid.UUID) -> Thought | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, thought_id: uuid.UUID) -> None:
        raise NotImplementedError
