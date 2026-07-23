"""Scans for tasks/calendar events due for a reminder and raises a
`Notification` for each (once per entity+kind — see
`NotificationRepositoryPort.exists`), mirrored by an email to the owner.
Runs with no per-request user context: triggered by Cloud Scheduler hitting
an internal endpoint, not a logged-in HTTP request.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from app.application.ports.calendar_port import CalendarPort
from app.application.ports.email_sender import EmailSenderPort
from app.application.ports.notification_repository import NotificationRepositoryPort
from app.application.ports.task_repository import TaskRepositoryPort
from app.application.ports.user_repository import UserRepositoryPort
from app.core.exceptions import AuthError, ExternalServiceError
from app.core.logging import get_logger
from app.domain.entities import NotificationKind, Task, TaskStatus, User

logger = get_logger(__name__)

DUE_SOON_WINDOW = timedelta(hours=24)
ENDING_SOON_WINDOW = timedelta(minutes=10)
"""How far ahead of a task's end time (`due_at`) to send the "time's almost
up" email — checked on whatever cadence Cloud Scheduler runs this sweep at,
so the actual lead time seen is anywhere from ENDING_SOON_WINDOW down to
(ENDING_SOON_WINDOW - sweep interval)."""

CALENDAR_NUDGE_WINDOW = timedelta(minutes=10)
"""How far ahead of a calendar event's start time to send the "starting
soon" nudge — same reasoning as ENDING_SOON_WINDOW: with a 5-minute sweep,
actual lead time seen is anywhere from CALENDAR_NUDGE_WINDOW down to
(CALENDAR_NUDGE_WINDOW - sweep interval), never zero."""


def _calendar_related_id(user_id: uuid.UUID, event_id: str) -> uuid.UUID:
    """Google Calendar event IDs are strings, but `Notification.related_id`
    is a UUID column shared with Task/Client notification kinds. This
    derives a stable dedup key from the event id — it's never decoded back,
    only compared for "have we already notified about this event"."""
    return uuid.uuid5(uuid.NAMESPACE_URL, f"gcal-start:{user_id}:{event_id}")


class CheckRemindersUseCase:
    def __init__(
        self,
        user_repository: UserRepositoryPort,
        task_repository: TaskRepositoryPort,
        notification_repository: NotificationRepositoryPort,
        email_sender: EmailSenderPort,
        calendar_port: CalendarPort,
    ) -> None:
        self._users = user_repository
        self._tasks = task_repository
        self._notifications = notification_repository
        self._email_sender = email_sender
        self._calendar = calendar_port

    async def execute(self) -> int:
        """Returns how many new notifications were raised this run."""
        now = datetime.now(UTC)
        due_soon_cutoff = now + DUE_SOON_WINDOW
        ending_soon_cutoff = now + ENDING_SOON_WINDOW
        raised = 0
        for user in await self._users.list_all():
            tasks = await self._tasks.list_by_user(user.id)
            raised += await self._check_tasks(
                user, tasks, now, due_soon_cutoff, ending_soon_cutoff
            )
            raised += await self._check_timers(user, tasks, now)
            raised += await self._check_calendar(user, now)
        return raised

    async def _check_tasks(
        self,
        user: User,
        tasks: list[Task],
        now: datetime,
        due_soon_cutoff: datetime,
        ending_soon_cutoff: datetime,
    ) -> int:
        raised = 0
        for task in tasks:
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

    async def _check_timers(self, user: User, tasks: list[Task], now: datetime) -> int:
        raised = 0
        for task in tasks:
            if (
                task.status != TaskStatus.IN_PROGRESS
                or task.timer_started_at is None
                or task.start_at is None
                or task.due_at is None
            ):
                continue
            deadline = task.timer_started_at + (task.due_at - task.start_at)
            if deadline > now:
                continue
            raised += await self._raise_once(
                user,
                NotificationKind.TASK_TIMER_EXPIRED,
                task.id,
                title=f"נגמר הזמן למשימה: {task.title}",
                body=f'הזמן שהוקצב למשימה "{task.title}" נגמר.',
            )
        return raised

    async def _check_calendar(self, user: User, now: datetime) -> int:
        raised = 0
        try:
            events = await self._calendar.list_between(
                user.id, now.isoformat(), (now + CALENDAR_NUDGE_WINDOW).isoformat()
            )
        except (AuthError, ExternalServiceError) as exc:
            # Best-effort: a not-yet-linked or expired Google account must
            # not stop task reminders for this user or abort the sweep.
            logger.warning("calendar_nudge_fetch_failed", error=str(exc), user_id=str(user.id))
            return 0
        for event in events:
            start = datetime.fromisoformat(event.start)
            raised += await self._raise_once(
                user,
                NotificationKind.CALENDAR_EVENT_STARTING,
                _calendar_related_id(user.id, event.id),
                title=f"מתחיל בעוד מעט: {event.summary}",
                body=f'האירוע "{event.summary}" מתחיל ב-{start:%H:%M}.',
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
