from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.entities import Task, TaskStatus


class TaskRepositoryPort(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: uuid.UUID,
        title: str,
        project_id: uuid.UUID | None = None,
        due_at: datetime | None = None,
        client_id: uuid.UUID | None = None,
        start_at: datetime | None = None,
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
    async def set_due_at(self, task_id: uuid.UUID, due_at: datetime | None) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def start_timer(self, task_id: uuid.UUID) -> Task:
        """Marks work as actually begun now: sets `timer_started_at` to the
        current time and `status` to `IN_PROGRESS`."""
        raise NotImplementedError

    @abstractmethod
    async def stop_timer(self, task_id: uuid.UUID) -> Task:
        """Cancels a running timer: clears `timer_started_at` and reverts
        `status` to `OPEN`."""
        raise NotImplementedError

    @abstractmethod
    async def update_details(
        self,
        task_id: uuid.UUID,
        title: str,
        due_at: datetime | None,
        project_id: uuid.UUID | None,
        client_id: uuid.UUID | None,
        start_at: datetime | None = None,
    ) -> Task:
        """A full-form save (edit modal), not a partial patch — every field
        is set exactly to what's given, `None` included, so clearing a
        project/client assignment or due date works as expected."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, task_id: uuid.UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def count_open(self, user_id: uuid.UUID) -> int:
        raise NotImplementedError
