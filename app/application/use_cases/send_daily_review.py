"""Sends a once-daily "did you actually do it" accountability email: for
Tasks (which have a real done/not-done state) this reports exactly what got
finished vs not; Google Calendar events have no completion concept, so
they're listed as a plain FYI, never claimed done or missed. Runs with no
per-request user context: triggered by Cloud Scheduler hitting an internal
endpoint, once a day, not a logged-in HTTP request.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from app.application.ports.calendar_port import CalendarPort
from app.application.ports.daily_plan_repository import DailyPlanRepositoryPort
from app.application.ports.email_sender import EmailSenderPort
from app.application.ports.notification_repository import NotificationRepositoryPort
from app.application.ports.task_repository import TaskRepositoryPort
from app.application.ports.user_repository import UserRepositoryPort
from app.core.exceptions import AuthError, ExternalServiceError
from app.core.logging import get_logger
from app.domain.entities import CalendarEvent, NotificationKind, Task, TaskStatus, User

logger = get_logger(__name__)


def _daily_review_related_id(user_id: uuid.UUID, day: datetime) -> uuid.UUID:
    """One review per user per calendar day — this dedup key is never
    decoded back, only compared for "did we already send today's review"."""
    return uuid.uuid5(uuid.NAMESPACE_URL, f"daily-review:{user_id}:{day.date().isoformat()}")


class SendDailyReviewUseCase:
    def __init__(
        self,
        user_repository: UserRepositoryPort,
        task_repository: TaskRepositoryPort,
        calendar_port: CalendarPort,
        notification_repository: NotificationRepositoryPort,
        email_sender: EmailSenderPort,
        daily_plan_repository: DailyPlanRepositoryPort,
        app_base_url: str = "",
    ) -> None:
        self._users = user_repository
        self._tasks = task_repository
        self._calendar = calendar_port
        self._notifications = notification_repository
        self._email_sender = email_sender
        self._plans = daily_plan_repository
        self._app_base_url = app_base_url

    async def execute(self) -> int:
        """Returns how many review emails were sent this run."""
        now = datetime.now(UTC)
        day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        sent = 0
        for user in await self._users.list_all():
            sent += await self._review_for_user(user, now, day_start, day_end)
        return sent

    async def _review_for_user(
        self, user: User, now: datetime, day_start: datetime, day_end: datetime
    ) -> int:
        related_id = _daily_review_related_id(user.id, now)
        if await self._notifications.exists(user.id, NotificationKind.DAILY_REVIEW, related_id):
            return 0

        tasks = await self._tasks.list_by_user(user.id)
        todays_tasks = [
            t for t in tasks if t.due_at is not None and day_start <= t.due_at < day_end
        ]
        done = [t for t in todays_tasks if t.status == TaskStatus.DONE]
        not_done = [t for t in todays_tasks if t.status != TaskStatus.DONE]

        try:
            events = await self._calendar.list_between(
                user.id, day_start.isoformat(), day_end.isoformat()
            )
        except (AuthError, ExternalServiceError) as exc:
            logger.warning(
                "daily_review_calendar_fetch_failed", error=str(exc), user_id=str(user.id)
            )
            events = []

        tomorrow_plan = await self._plans.get_by_date(user.id, day_start.date() + timedelta(days=1))
        tomorrow_locked = tomorrow_plan is not None and tomorrow_plan.is_locked

        if not todays_tasks and not events and tomorrow_locked:
            return 0

        title = "סיכום יומי: מה בוצע ומה לא"
        body = self._compose_body(done, not_done, events, tomorrow_locked)

        await self._notifications.create(
            user.id, NotificationKind.DAILY_REVIEW, related_id, title, body
        )
        try:
            await self._email_sender.send(user.id, user.email, title, body)
        except (AuthError, ExternalServiceError) as exc:
            logger.warning("daily_review_email_failed", error=str(exc), user_id=str(user.id))
        return 1

    def _compose_body(
        self,
        done: list[Task],
        not_done: list[Task],
        events: list[CalendarEvent],
        tomorrow_locked: bool,
    ) -> str:
        lines: list[str] = [f"הושלם היום ({len(done)}):"]
        lines.extend([f"✔ {t.title}" for t in done] or ["— אין"])
        lines.append("")
        lines.append(f"לא הושלם ({len(not_done)}):")
        lines.extend([f"✘ {t.title}" for t in not_done] or ["— אין"])
        lines.append("")
        lines.append("ליומן (למידע בלבד, לא נבדק ביצוע):")
        lines.extend([f"• {e.summary}" for e in events] or ["— אין אירועים"])
        lines.append("")
        if tomorrow_locked:
            lines.append(
                "המשימה הראשונה למחר כבר נעולה. כשתפתח את האפליקציה מחר, "
                "היא תיפתח ישר אליה."
            )
        else:
            lines.append(
                "עוד לא נעלת משימה ראשונה למחר — זה הרגע לעשות את זה, "
                "לפני שהיום מתחיל ואתה צריך להחליט."
            )
            if self._app_base_url:
                lines.append(self._app_base_url)
        return "\n".join(lines)
