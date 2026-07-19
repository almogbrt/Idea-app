from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import Notification, NotificationKind


class NotificationRepositoryPort(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: uuid.UUID,
        kind: NotificationKind,
        related_id: uuid.UUID,
        title: str,
        body: str,
    ) -> Notification:
        raise NotImplementedError

    @abstractmethod
    async def exists(
        self, user_id: uuid.UUID, kind: NotificationKind, related_id: uuid.UUID
    ) -> bool:
        """Whether a notification of this kind was already raised for this
        entity — the idempotency check that stops a reminder from firing
        more than once for the same due date."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, notification_id: uuid.UUID) -> Notification | None:
        raise NotImplementedError

    @abstractmethod
    async def list_unread(self, user_id: uuid.UUID) -> list[Notification]:
        raise NotImplementedError

    @abstractmethod
    async def mark_read(self, notification_id: uuid.UUID) -> Notification:
        raise NotImplementedError

    @abstractmethod
    async def mark_all_read(self, user_id: uuid.UUID) -> None:
        raise NotImplementedError
