from __future__ import annotations

import uuid

from app.application.ports.notification_repository import NotificationRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import Notification


class ManageNotificationsUseCase:
    def __init__(self, notification_repository: NotificationRepositoryPort) -> None:
        self._notifications = notification_repository

    async def list_unread(self, user_id: uuid.UUID) -> list[Notification]:
        return await self._notifications.list_unread(user_id)

    async def get_or_raise(self, notification_id: uuid.UUID) -> Notification:
        notification = await self._notifications.get(notification_id)
        if notification is None:
            raise NotFoundError(
                "Notification not found", details={"notification_id": str(notification_id)}
            )
        return notification

    async def mark_read(self, notification_id: uuid.UUID) -> Notification:
        return await self._notifications.mark_read(notification_id)

    async def mark_all_read(self, user_id: uuid.UUID) -> None:
        await self._notifications.mark_all_read(user_id)
