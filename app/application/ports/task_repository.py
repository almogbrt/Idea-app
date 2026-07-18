from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import Task, TaskStatus


class TaskRepositoryPort(ABC):
    @abstractmethod
    async def create(
        self, user_id: uuid.UUID, title: str, project_id: uuid.UUID | None = None
    ) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: uuid.UUID) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, task_id: uuid.UUID) -> Task | None:
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, task_id: uuid.UUID, status: TaskStatus) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def count_open(self, user_id: uuid.UUID) -> int:
        raise NotImplementedError
