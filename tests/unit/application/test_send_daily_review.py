from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.application.use_cases.send_daily_review import SendDailyReviewUseCase
from app.core.exceptions import AuthError
from app.domain.entities import NotificationKind, TaskStatus
from tests.conftest import (
    FakeCalendarPort,
    FakeDailyPlanRepository,
    FakeNotificationRepository,
    FakeTaskRepository,
    FakeUserRepository,
)


class _FakeEmailSender:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    async def send(self, user_id: object, to: str, subject: str, body: str) -> None:
        self.sent.append((subject, body))


def _make_use_case(
    users: FakeUserRepository,
    tasks: FakeTaskRepository,
    calendar: FakeCalendarPort,
    notifications: FakeNotificationRepository,
    email_sender: _FakeEmailSender,
    daily_plans: FakeDailyPlanRepository | None = None,
) -> SendDailyReviewUseCase:
    return SendDailyReviewUseCase(
        users,
        tasks,
        calendar,
        notifications,
        email_sender,
        daily_plans if daily_plans is not None else FakeDailyPlanRepository(),
        app_base_url="https://idea-os.example.com",
    )


async def test_reports_done_and_not_done_tasks_for_today(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_calendar_port: FakeCalendarPort,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user = await fake_user_repository.create("sub-1", "owner@example.com", "Owner")
    now = datetime.now(UTC)
    today_9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
    done_task = await fake_task_repository.create(
        user.id, "Finished task", start_at=today_9am, due_at=today_9am + timedelta(hours=1)
    )
    await fake_task_repository.update_status(done_task.id, TaskStatus.DONE)
    await fake_task_repository.create(
        user.id,
        "Unfinished task",
        start_at=today_9am + timedelta(hours=2),
        due_at=today_9am + timedelta(hours=3),
    )

    email_sender = _FakeEmailSender()
    use_case = _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_calendar_port,
        fake_notification_repository,
        email_sender,
    )

    sent = await use_case.execute()

    assert sent == 1
    subject, body = email_sender.sent[0]
    assert "Finished task" in body
    assert "Unfinished task" in body
    unread = await fake_notification_repository.list_unread(user.id)
    assert unread[0].kind == NotificationKind.DAILY_REVIEW


async def test_lists_calendar_events_as_fyi_without_completion_claim(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_calendar_port: FakeCalendarPort,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user = await fake_user_repository.create("sub-2", "owner2@example.com", "Owner")
    now = datetime.now(UTC)
    await fake_calendar_port.create(
        user.id,
        "Client meeting",
        (now.replace(hour=10, minute=0)).isoformat(),
        (now.replace(hour=11, minute=0)).isoformat(),
    )

    email_sender = _FakeEmailSender()
    use_case = _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_calendar_port,
        fake_notification_repository,
        email_sender,
    )

    sent = await use_case.execute()

    assert sent == 1
    _, body = email_sender.sent[0]
    assert "Client meeting" in body


async def test_prompts_to_lock_tomorrow_even_with_nothing_today(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_calendar_port: FakeCalendarPort,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    """Even with nothing due today and no calendar events, the email still
    goes out — its job now is also to prompt locking tomorrow's first task,
    which is always relevant until that's done."""
    await fake_user_repository.create("sub-3", "owner3@example.com", "Owner")
    email_sender = _FakeEmailSender()
    use_case = _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_calendar_port,
        fake_notification_repository,
        email_sender,
    )

    sent = await use_case.execute()

    assert sent == 1
    _, body = email_sender.sent[0]
    assert "לא נעלת משימה ראשונה למחר" in body
    assert "https://idea-os.example.com" in body


async def test_skips_users_with_nothing_today_and_tomorrow_already_locked(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_calendar_port: FakeCalendarPort,
    fake_notification_repository: FakeNotificationRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
) -> None:
    user = await fake_user_repository.create("sub-3b", "owner3b@example.com", "Owner")
    tomorrow = datetime.now(UTC).date() + timedelta(days=1)
    plan = await fake_daily_plan_repository.create(user.id, tomorrow)
    task = await fake_task_repository.create(user.id, "Tomorrow's task")
    await fake_daily_plan_repository.set_main_task(plan.id, task.id)
    await fake_daily_plan_repository.lock(plan.id)

    email_sender = _FakeEmailSender()
    use_case = _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_calendar_port,
        fake_notification_repository,
        email_sender,
        fake_daily_plan_repository,
    )

    sent = await use_case.execute()

    assert sent == 0
    assert email_sender.sent == []


async def test_notes_tomorrow_already_locked_in_body(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_calendar_port: FakeCalendarPort,
    fake_notification_repository: FakeNotificationRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
) -> None:
    user = await fake_user_repository.create("sub-3c", "owner3c@example.com", "Owner")
    tomorrow = datetime.now(UTC).date() + timedelta(days=1)
    plan = await fake_daily_plan_repository.create(user.id, tomorrow)
    tomorrow_task = await fake_task_repository.create(user.id, "Tomorrow's task")
    await fake_daily_plan_repository.set_main_task(plan.id, tomorrow_task.id)
    await fake_daily_plan_repository.lock(plan.id)
    now = datetime.now(UTC)
    await fake_task_repository.create(
        user.id, "Today's task", start_at=now, due_at=now + timedelta(hours=1)
    )

    email_sender = _FakeEmailSender()
    use_case = _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_calendar_port,
        fake_notification_repository,
        email_sender,
        fake_daily_plan_repository,
    )

    sent = await use_case.execute()

    assert sent == 1
    _, body = email_sender.sent[0]
    assert "כבר נעולה" in body


async def test_is_idempotent_across_repeated_runs_same_day(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_calendar_port: FakeCalendarPort,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user = await fake_user_repository.create("sub-4", "owner4@example.com", "Owner")
    now = datetime.now(UTC)
    await fake_task_repository.create(
        user.id, "Task", start_at=now, due_at=now + timedelta(hours=1)
    )
    email_sender = _FakeEmailSender()
    use_case = _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_calendar_port,
        fake_notification_repository,
        email_sender,
    )

    first_run = await use_case.execute()
    second_run = await use_case.execute()

    assert first_run == 1
    assert second_run == 0
    assert len(email_sender.sent) == 1


async def test_survives_calendar_fetch_failure(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user = await fake_user_repository.create("sub-5", "owner5@example.com", "Owner")
    now = datetime.now(UTC)
    await fake_task_repository.create(
        user.id, "Task", start_at=now, due_at=now + timedelta(hours=1)
    )
    failing_calendar = FakeCalendarPort(fail_with=AuthError)
    email_sender = _FakeEmailSender()
    use_case = _make_use_case(
        fake_user_repository,
        fake_task_repository,
        failing_calendar,
        fake_notification_repository,
        email_sender,
    )

    sent = await use_case.execute()

    assert sent == 1
    _, body = email_sender.sent[0]
    assert "Task" in body
