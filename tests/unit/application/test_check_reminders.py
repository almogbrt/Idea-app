from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from app.application.ports.email_sender import EmailSenderPort
from app.application.use_cases.check_reminders import CheckRemindersUseCase
from app.application.use_cases.manage_notifications import ManageNotificationsUseCase
from app.core.exceptions import AppError, AuthError, ExternalServiceError
from app.domain.entities import NotificationKind, TaskStatus
from tests.conftest import (
    FakeClientRepository,
    FakeNotificationRepository,
    FakeTaskRepository,
    FakeUserRepository,
)


class _FakeEmailSender(EmailSenderPort):
    def __init__(self, *, fail_with: type[AppError] | None = None) -> None:
        self.sent: list[tuple[uuid.UUID, str, str, str]] = []
        self._fail_with = fail_with

    async def send(self, user_id: uuid.UUID, to: str, subject: str, body: str) -> None:
        if self._fail_with is not None:
            raise self._fail_with("Gmail is unavailable")
        self.sent.append((user_id, to, subject, body))


async def _make_use_case(
    users: FakeUserRepository,
    tasks: FakeTaskRepository,
    clients: FakeClientRepository,
    notifications: FakeNotificationRepository,
    email_sender: EmailSenderPort,
) -> CheckRemindersUseCase:
    return CheckRemindersUseCase(users, tasks, clients, notifications, email_sender)


async def test_raises_overdue_notification_and_sends_email(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_repository: FakeClientRepository,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user = await fake_user_repository.create("sub-1", "owner@example.com", "Owner")
    await fake_task_repository.create(
        user.id, "Overdue task", due_at=datetime.now(UTC) - timedelta(days=1)
    )
    email_sender = _FakeEmailSender()
    use_case = await _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_client_repository,
        notifications=fake_notification_repository,
        email_sender=email_sender,
    )

    raised = await use_case.execute()

    assert raised == 1
    unread = await fake_notification_repository.list_unread(user.id)
    assert len(unread) == 1
    assert unread[0].kind == NotificationKind.TASK_OVERDUE
    assert len(email_sender.sent) == 1
    assert email_sender.sent[0][1] == "owner@example.com"


async def test_raises_due_soon_notification_for_task_due_within_24h(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_repository: FakeClientRepository,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user = await fake_user_repository.create("sub-2", "owner2@example.com", "Owner")
    await fake_task_repository.create(
        user.id, "Soon task", due_at=datetime.now(UTC) + timedelta(hours=2)
    )
    use_case = await _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_client_repository,
        notifications=fake_notification_repository,
        email_sender=_FakeEmailSender(),
    )

    raised = await use_case.execute()

    assert raised == 1
    unread = await fake_notification_repository.list_unread(user.id)
    assert unread[0].kind == NotificationKind.TASK_DUE_SOON


async def test_does_not_notify_for_done_task_or_far_future_task(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_repository: FakeClientRepository,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user = await fake_user_repository.create("sub-3", "owner3@example.com", "Owner")
    far_future_task = await fake_task_repository.create(
        user.id, "Later task", due_at=datetime.now(UTC) + timedelta(days=10)
    )
    done_task = await fake_task_repository.create(
        user.id, "Done overdue task", due_at=datetime.now(UTC) - timedelta(days=1)
    )
    await fake_task_repository.update_status(done_task.id, TaskStatus.DONE)

    use_case = await _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_client_repository,
        notifications=fake_notification_repository,
        email_sender=_FakeEmailSender(),
    )

    raised = await use_case.execute()

    assert raised == 0
    assert far_future_task.due_at is not None  # sanity: task was created with a due date


async def test_is_idempotent_across_repeated_runs(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_repository: FakeClientRepository,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user = await fake_user_repository.create("sub-4", "owner4@example.com", "Owner")
    await fake_task_repository.create(
        user.id, "Overdue task", due_at=datetime.now(UTC) - timedelta(days=1)
    )
    email_sender = _FakeEmailSender()
    use_case = await _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_client_repository,
        notifications=fake_notification_repository,
        email_sender=email_sender,
    )

    first_run = await use_case.execute()
    second_run = await use_case.execute()

    assert first_run == 1
    assert second_run == 0
    assert len(email_sender.sent) == 1


async def test_raises_client_follow_up_notification(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_repository: FakeClientRepository,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user = await fake_user_repository.create("sub-5", "owner5@example.com", "Owner")
    client = await fake_client_repository.create(user.id, "Baron's")
    await fake_client_repository.update(
        client.id, next_follow_up_at=datetime.now(UTC) - timedelta(hours=1)
    )

    use_case = await _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_client_repository,
        notifications=fake_notification_repository,
        email_sender=_FakeEmailSender(),
    )

    raised = await use_case.execute()

    assert raised == 1
    unread = await fake_notification_repository.list_unread(user.id)
    assert unread[0].kind == NotificationKind.CLIENT_FOLLOW_UP_DUE


async def test_survives_email_send_failure(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_repository: FakeClientRepository,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    """Email delivery is best-effort — a down Gmail connection must not stop
    the notification itself from being raised (it'll still show in the
    dashboard bell)."""
    user = await fake_user_repository.create("sub-6", "owner6@example.com", "Owner")
    await fake_task_repository.create(
        user.id, "Overdue task", due_at=datetime.now(UTC) - timedelta(days=1)
    )
    use_case = await _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_client_repository,
        notifications=fake_notification_repository,
        email_sender=_FakeEmailSender(fail_with=ExternalServiceError),
    )

    raised = await use_case.execute()

    assert raised == 1
    unread = await fake_notification_repository.list_unread(user.id)
    assert len(unread) == 1


async def test_survives_email_send_failure_when_google_account_not_linked(
    fake_user_repository: FakeUserRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_repository: FakeClientRepository,
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    """Regression test: an owner who hasn't linked Google yet (or whose token
    expired) makes `GmailClient.send_message` raise `AuthError`, not
    `ExternalServiceError` — that must not abort the rest of the sweep either,
    or every other due task/client silently stops getting notified."""
    user = await fake_user_repository.create("sub-7", "owner7@example.com", "Owner")
    await fake_task_repository.create(
        user.id, "Overdue task", due_at=datetime.now(UTC) - timedelta(days=1)
    )
    await fake_task_repository.create(
        user.id, "Another overdue task", due_at=datetime.now(UTC) - timedelta(days=2)
    )
    use_case = await _make_use_case(
        fake_user_repository,
        fake_task_repository,
        fake_client_repository,
        notifications=fake_notification_repository,
        email_sender=_FakeEmailSender(fail_with=AuthError),
    )

    raised = await use_case.execute()

    assert raised == 2
    unread = await fake_notification_repository.list_unread(user.id)
    assert len(unread) == 2


async def test_manage_notifications_list_and_mark_read(
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user_id = uuid.uuid4()
    notification = await fake_notification_repository.create(
        user_id, NotificationKind.TASK_OVERDUE, uuid.uuid4(), "Title", "Body"
    )
    use_case = ManageNotificationsUseCase(fake_notification_repository)

    unread_before = await use_case.list_unread(user_id)
    assert len(unread_before) == 1

    await use_case.mark_read(notification.id)
    unread_after = await use_case.list_unread(user_id)
    assert unread_after == []


async def test_manage_notifications_mark_all_read(
    fake_notification_repository: FakeNotificationRepository,
) -> None:
    user_id = uuid.uuid4()
    await fake_notification_repository.create(
        user_id, NotificationKind.TASK_OVERDUE, uuid.uuid4(), "T1", "B1"
    )
    await fake_notification_repository.create(
        user_id, NotificationKind.TASK_DUE_SOON, uuid.uuid4(), "T2", "B2"
    )
    use_case = ManageNotificationsUseCase(fake_notification_repository)

    await use_case.mark_all_read(user_id)

    assert await use_case.list_unread(user_id) == []
