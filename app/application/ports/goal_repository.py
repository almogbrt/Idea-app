from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import Goal


class GoalRepositoryPort(ABC):
    @abstractmethod
    async def create(self, user_id: uuid.UUID, name: str) -> Goal:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: uuid.UUID) -> list[Goal]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, goal_id: uuid.UUID) -> Goal | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, goal_id: uuid.UUID, name: str) -> Goal:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, goal_id: uuid.UUID) -> None:
        raise NotImplementedError
