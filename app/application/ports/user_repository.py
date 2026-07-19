from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import User


class UserRepositoryPort(ABC):
    @abstractmethod
    async def get_by_google_sub(self, google_sub: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, google_sub: str, email: str, name: str) -> User:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> list[User]:
        raise NotImplementedError
