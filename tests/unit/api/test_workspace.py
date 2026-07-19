from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from app.application.ports.email_sender import EmailSenderPort
from app.application.ports.inbox import InboxPort
from app.application.ports.schedule import SchedulePort
from app.application.use_cases.check_reminders import CheckRemindersUseCase
from app.application.use_cases.manage_notifications import ManageNotificationsUseCase
from app.application.use_cases.manage_workspace import (
    DashboardSummaryUseCase,
    ListActivityUseCase,
    ManageClientsUseCase,
    ManageProjectsUseCase,
    ManageTasksUseCase,
)
from app.core import config as config_module
from app.core.container import RequestScopedServices
from app.domain.entities import NotificationKind, User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from tests.conftest import (
    FakeAgentExecutionRepository,
    FakeClientRepository,
    FakeNotificationRepository,
    FakeProjectRepository,
    FakeTaskRepository,
    FakeUserRepository,
)

_USER = User(
    id=uuid.uuid4(),
    google_sub="sub-workspace",
    email="owner@example.com",
    name="Owner",
    created_at=datetime.now(UTC),
)


class _NullInbox(InboxPort):
    async def count_unread(self, user_id: uuid.UUID) -> int:
        return 3


class _NullSchedule(SchedulePort):
    async def count_meetings_today(self, user_id: uuid.UUID) -> int:
        return 1


class _NullOrchestrator:
    async def handle_command(self, **kwargs: object) -> None:
        raise NotImplementedError


class _NullEmailSender(EmailSenderPort):
    async def send(self, user_id: uuid.UUID, to: str, subject: str, body: str) -> None:
        return None


def _install_scope(client: TestClient) -> dict[str, object]:
    clients_repo = FakeClientRepository()
    projects_repo = FakeProjectRepository()
    tasks_repo = FakeTaskRepository()
    executions_repo = FakeAgentExecutionRepository()
    notifications_repo = FakeNotificationRepository()
    users_repo = FakeUserRepository()

    scope = RequestScopedServices(
        orchestrator=_NullOrchestrator(),  # type: ignore[arg-type]
        manage_conversation=None,  # type: ignore[arg-type]
        authenticate_user=None,  # type: ignore[arg-type]
        manage_clients=ManageClientsUseCase(clients_repo, projects_repo, tasks_repo),
        manage_projects=ManageProjectsUseCase(projects_repo),
        manage_tasks=ManageTasksUseCase(tasks_repo),
        dashboard_summary=DashboardSummaryUseCase(
            projects_repo, tasks_repo, _NullInbox(), _NullSchedule()
        ),
        list_activity=ListActivityUseCase(executions_repo),
        manage_notifications=ManageNotificationsUseCase(notifications_repo),
        check_reminders=CheckRemindersUseCase(
            users_repo, tasks_repo, clients_repo, notifications_repo, _NullEmailSender()
        ),
    )
    client.app.dependency_overrides[get_current_user] = lambda: _USER
    client.app.dependency_overrides[get_request_scope] = lambda: scope
    return {
        "clients_repo": clients_repo,
        "projects_repo": projects_repo,
        "tasks_repo": tasks_repo,
        "executions_repo": executions_repo,
        "notifications_repo": notifications_repo,
    }


def test_dashboard_summary_returns_counts_and_live_stats(client: TestClient) -> None:
    _install_scope(client)

    response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "open_tasks": 0,
        "active_projects": 0,
        "unread_emails": 3,
        "meetings_today": 1,
    }


def test_dashboard_requires_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 401


def test_create_and_list_clients(client: TestClient) -> None:
    _install_scope(client)

    create_response = client.post("/api/v1/clients", json={"name": "Baron's"})
    assert create_response.status_code == 200
    assert create_response.json()["name"] == "Baron's"

    list_response = client.get("/api/v1/clients")
    assert [c["name"] for c in list_response.json()] == ["Baron's"]


def test_create_and_list_projects(client: TestClient) -> None:
    _install_scope(client)

    create_response = client.post("/api/v1/projects", json={"name": "Summer menu"})
    assert create_response.status_code == 200
    body = create_response.json()
    assert body["name"] == "Summer menu"
    assert body["status"] == "in_progress"
    assert body["client_name"] is None

    list_response = client.get("/api/v1/projects")
    assert len(list_response.json()) == 1


def test_update_project_status(client: TestClient) -> None:
    _install_scope(client)
    project = client.post("/api/v1/projects", json={"name": "Rebrand"}).json()

    response = client.patch(
        f"/api/v1/projects/{project['id']}/status", json={"status": "on_hold"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "on_hold"


def test_update_project_status_rejects_other_users_project(client: TestClient) -> None:
    resources = _install_scope(client)
    other_user_project = client.post("/api/v1/projects", json={"name": "Not yours"}).json()

    # simulate the project belonging to someone else by mutating the fake repo directly
    projects_repo = resources["projects_repo"]
    stored = projects_repo.projects[uuid.UUID(other_user_project["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.patch(
        f"/api/v1/projects/{other_user_project['id']}/status", json={"status": "done"}
    )

    assert response.status_code == 403


def test_create_and_toggle_task(client: TestClient) -> None:
    _install_scope(client)
    task = client.post("/api/v1/tasks", json={"title": "Prep summer menu"}).json()
    assert task["status"] == "open"

    response = client.patch(f"/api/v1/tasks/{task['id']}/status", json={"status": "done"})

    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_update_task_status_rejects_other_users_task(client: TestClient) -> None:
    resources = _install_scope(client)
    task = client.post("/api/v1/tasks", json={"title": "Not yours"}).json()

    tasks_repo = resources["tasks_repo"]
    stored = tasks_repo.tasks[uuid.UUID(task["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.patch(f"/api/v1/tasks/{task['id']}/status", json={"status": "done"})

    assert response.status_code == 403


def test_dashboard_activity_reflects_only_current_user(client: TestClient) -> None:
    _install_scope(client)
    response = client.get("/api/v1/dashboard/activity")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task_with_due_at_and_update_due_date(client: TestClient) -> None:
    _install_scope(client)
    task = client.post(
        "/api/v1/tasks", json={"title": "Send invoice", "due_at": "2026-08-01T09:00:00Z"}
    ).json()
    assert task["due_at"] is not None

    response = client.patch(
        f"/api/v1/tasks/{task['id']}/due-date", json={"due_at": "2026-09-01T09:00:00Z"}
    )

    assert response.status_code == 200
    assert response.json()["due_at"].startswith("2026-09-01")


def test_update_task_due_at_rejects_other_users_task(client: TestClient) -> None:
    resources = _install_scope(client)
    task = client.post("/api/v1/tasks", json={"title": "Not yours"}).json()

    tasks_repo = resources["tasks_repo"]
    stored = tasks_repo.tasks[uuid.UUID(task["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.patch(
        f"/api/v1/tasks/{task['id']}/due-date", json={"due_at": "2026-09-01T09:00:00Z"}
    )

    assert response.status_code == 403


async def test_notifications_list_mark_read_and_mark_all_read(client: TestClient) -> None:
    resources = _install_scope(client)
    notifications_repo: FakeNotificationRepository = resources["notifications_repo"]  # type: ignore[assignment]

    n1 = await notifications_repo.create(
        _USER.id, NotificationKind.TASK_OVERDUE, uuid.uuid4(), "Overdue", "body"
    )
    await notifications_repo.create(
        _USER.id, NotificationKind.TASK_DUE_SOON, uuid.uuid4(), "Soon", "body"
    )

    listed = client.get("/api/v1/notifications").json()
    assert len(listed) == 2

    read_response = client.patch(f"/api/v1/notifications/{n1.id}/read")
    assert read_response.status_code == 200
    assert read_response.json()["read_at"] is not None

    after_one_read = client.get("/api/v1/notifications").json()
    assert len(after_one_read) == 1

    mark_all = client.post("/api/v1/notifications/read-all")
    assert mark_all.status_code == 204

    after_all_read = client.get("/api/v1/notifications").json()
    assert after_all_read == []


async def test_mark_notification_read_rejects_other_users_notification(
    client: TestClient,
) -> None:
    resources = _install_scope(client)
    notifications_repo: FakeNotificationRepository = resources["notifications_repo"]  # type: ignore[assignment]

    notification = await notifications_repo.create(
        uuid.uuid4(), NotificationKind.TASK_OVERDUE, uuid.uuid4(), "Not yours", "body"
    )

    response = client.patch(f"/api/v1/notifications/{notification.id}/read")

    assert response.status_code == 403


def test_run_reminders_requires_scheduler_secret(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    _install_scope(client)
    monkeypatch.setenv("SCHEDULER_SHARED_SECRET", "test-secret")
    config_module.get_settings.cache_clear()

    try:
        unauthorized = client.post("/api/v1/internal/reminders/run")
        assert unauthorized.status_code == 401

        wrong_secret = client.post(
            "/api/v1/internal/reminders/run", headers={"X-Scheduler-Secret": "wrong"}
        )
        assert wrong_secret.status_code == 401

        authorized = client.post(
            "/api/v1/internal/reminders/run", headers={"X-Scheduler-Secret": "test-secret"}
        )
        assert authorized.status_code == 200
        assert "notifications_raised" in authorized.json()
    finally:
        config_module.get_settings.cache_clear()
