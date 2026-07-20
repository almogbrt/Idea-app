"""Scans for tasks/clients due for a reminder and raises a `Notification` for
each (once per entity+kind — see `NotificationRepositoryPort.exists`), mirrored
by an email to the owner. Runs with no per-request user context: triggered by
Cloud Scheduler hitting an internal endpoint, not a logged-in HTTP request.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from app.application.ports.email_sender import EmailSenderPort
from app.application.ports.notification_repository import NotificationRepositoryPort
from app.application.ports.task_repository import TaskRepositoryPort
from app.application.ports.user_repository import UserRepositoryPort
from app.core.exceptions import AuthError, ExternalServiceError
from app.core.logging import get_logger
from app.domain.entities import NotificationKind, TaskStatus, User

logger = get_logger(__name__)

DUE_SOON_WINDOW = timedelta(hours=24)
ENDING_SOON_WINDOW = timedelta(minutes=10)
"""How far ahead of a task's end time (`due_at`) to send the "time's almost
up" email — checked on whatever cadence Cloud Scheduler runs this sweep at,
so the actual lead time seen is anywhere from ENDING_SOON_WINDOW down to
(ENDING_SOON_WINDOW - sweep interval)."""


class CheckRemindersUseCase:
    def __init__(
        self,
        user_repository: UserRepositoryPort,
        task_repository: TaskRepositoryPort,
        notification_repository: NotificationRepositoryPort,
        email_sender: EmailSenderPort,
    ) -> None:
        self._users = user_repository
        self._tasks = task_repository
        self._notifications = notification_repository
        self._email_sender = email_sender

    async def execute(self) -> int:
        """Returns how many new notifications were raised this run."""
        now = datetime.now(UTC)
        due_soon_cutoff = now + DUE_SOON_WINDOW
        ending_soon_cutoff = now + ENDING_SOON_WINDOW
        raised = 0
        for user in await self._users.list_all():
            raised += await self._check_tasks(user, now, due_soon_cutoff, ending_soon_cutoff)
        return raised

    async def _check_tasks(
        self, user: User, now: datetime, due_soon_cutoff: datetime, ending_soon_cutoff: datetime
    ) -> int:
        raised = 0
        for task in await self._tasks.list_by_user(user.id):
            if task.due_at is None or task.status == TaskStatus.DONE:
                continue
            if task.due_at < now:
                raised += await self._raise_once(
                    user,
                    NotificationKind.TASK_OVERDUE,
                    task.id,
                    title=f"משימה באיחור: {task.title}",
                    body=(
                        f'המשימה "{task.title}" הייתה אמורה להסתיים '
                        f"ב-{task.due_at:%d/%m/%Y %H:%M} וטרם סומנה כהושלמה."
                    ),
                )
                continue
            if task.due_at <= ending_soon_cutoff:
                raised += await self._raise_once(
                    user,
                    NotificationKind.TASK_ENDING_SOON,
                    task.id,
                    title=f"נגמר הזמן בעוד מעט: {task.title}",
                    body=(
                        f'פחות מ-10 דקות למשימה "{task.title}" '
                        f"(סיום ב-{task.due_at:%H:%M})."
                    ),
                )
            if task.due_at <= due_soon_cutoff:
                raised += await self._raise_once(
                    user,
                    NotificationKind.TASK_DUE_SOON,
                    task.id,
                    title=f"משימה מתקרבת: {task.title}",
                    body=f'המשימה "{task.title}" מתוכננת להסתיים ב-{task.due_at:%d/%m/%Y %H:%M}.',
                )
        return raised

    async def _raise_once(
        self, user: User, kind: NotificationKind, related_id: uuid.UUID, *, title: str, body: str
    ) -> int:
        if await self._notifications.exists(user.id, kind, related_id):
            return 0
        await self._notifications.create(user.id, kind, related_id, title, body)
        try:
            await self._email_sender.send(user.id, user.email, title, body)
        except (AuthError, ExternalServiceError) as exc:
            # Best-effort: a down/unlinked Gmail connection must not stop the
            # notification itself (still visible in the dashboard bell) or
            # abort the rest of this sweep.
            logger.warning("reminder_email_failed", error=str(exc), user_id=str(user.id))
        return 1
