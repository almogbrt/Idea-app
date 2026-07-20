from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from app.application.ports.calendar_port import CalendarPort
from app.application.ports.drive_port import DrivePort
from app.application.ports.email_sender import EmailSenderPort
from app.application.ports.inbox import InboxPort
from app.application.ports.schedule import SchedulePort
from app.application.use_cases.check_reminders import CheckRemindersUseCase
from app.application.use_cases.manage_calendar import ManageCalendarUseCase
from app.application.use_cases.manage_files import ManageFilesUseCase
from app.application.use_cases.manage_notifications import ManageNotificationsUseCase
from app.application.use_cases.manage_whatsapp_messages import ManageWhatsAppMessagesUseCase
from app.application.use_cases.manage_workspace import (
    DashboardSummaryUseCase,
    ListActivityUseCase,
    ManageClientsUseCase,
    ManageProjectsUseCase,
    ManageTasksUseCase,
    ManageThoughtsUseCase,
)
from app.core import config as config_module
from app.core.container import RequestScopedServices
from app.domain.entities import CalendarEvent, DriveFile, NotificationKind, User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from tests.conftest import (
    FakeAgentExecutionRepository,
    FakeClientLogoStorage,
    FakeClientRepository,
    FakeNotificationRepository,
    FakeProjectRepository,
    FakeTaskRepository,
    FakeThoughtRepository,
    FakeUserRepository,
    FakeWhatsAppMessageRepository,
)


def _task_payload(**overrides: object) -> dict[str, object]:
    """Every task the REST API creates now requires start_at/due_at — this
    fills in valid defaults so tests only spell out what they're actually
    exercising."""
    payload: dict[str, object] = {
        "title": "Task",
        "start_at": "2026-08-01T08:00:00Z",
        "due_at": "2026-08-01T09:00:00Z",
    }
    payload.update(overrides)
    return payload


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


class _FakeCalendar(CalendarPort):
    def __init__(self) -> None:
        self.events: dict[str, CalendarEvent] = {}

    async def list_between(
        self, user_id: uuid.UUID, time_min: str, time_max: str
    ) -> list[CalendarEvent]:
        return list(self.events.values())

    async def create(
        self,
        user_id: uuid.UUID,
        summary: str,
        start_time: str,
        end_time: str,
        description: str | None = None,
    ) -> CalendarEvent:
        event = CalendarEvent(
            id=str(uuid.uuid4()), summary=summary, start=start_time, end=end_time,
            description=description,
        )
        self.events[event.id] = event
        return event

    async def delete(self, user_id: uuid.UUID, event_id: str) -> None:
        self.events.pop(event_id, None)


class _FakeDrive(DrivePort):
    def __init__(self) -> None:
        self.files: dict[str, DriveFile] = {}
        self.shares: list[tuple[str, str, str]] = []

    async def list_files(
        self,
        user_id: uuid.UUID,
        query: str | None,
        max_results: int,
        order_by: str | None = None,
    ) -> list[DriveFile]:
        return list(self.files.values())[:max_results]

    async def get_content(self, user_id: uuid.UUID, file_id: str) -> str:
        return "file content"

    async def create_file(
        self, user_id: uuid.UUID, name: str, content: str, mime_type: str
    ) -> DriveFile:
        file = DriveFile(id=str(uuid.uuid4()), name=name, mime_type=mime_type)
        self.files[file.id] = file
        return file

    async def share_file(self, user_id: uuid.UUID, file_id: str, email: str, role: str) -> None:
        self.shares.append((file_id, email, role))


def _install_scope(client: TestClient) -> dict[str, object]:
    clients_repo = FakeClientRepository()
    projects_repo = FakeProjectRepository(clients_repo)
    tasks_repo = FakeTaskRepository()
    thoughts_repo = FakeThoughtRepository()
    whatsapp_messages_repo = FakeWhatsAppMessageRepository()
    executions_repo = FakeAgentExecutionRepository()
    notifications_repo = FakeNotificationRepository()
    users_repo = FakeUserRepository()
    calendar_port = _FakeCalendar()
    drive_port = _FakeDrive()
    logo_storage = FakeClientLogoStorage()

    scope = RequestScopedServices(
        orchestrator=_NullOrchestrator(),  # type: ignore[arg-type]
        manage_conversation=None,  # type: ignore[arg-type]
        authenticate_user=None,  # type: ignore[arg-type]
        manage_clients=ManageClientsUseCase(clients_repo, projects_repo, tasks_repo, logo_storage),
        manage_projects=ManageProjectsUseCase(projects_repo),
        manage_tasks=ManageTasksUseCase(tasks_repo),
        manage_thoughts=ManageThoughtsUseCase(thoughts_repo),
        manage_whatsapp_messages=ManageWhatsAppMessagesUseCase(whatsapp_messages_repo),
        dashboard_summary=DashboardSummaryUseCase(
            projects_repo, tasks_repo, clients_repo, _NullInbox(), _NullSchedule()
        ),
        manage_calendar=ManageCalendarUseCase(calendar_port),
        manage_files=ManageFilesUseCase(drive_port),
        list_activity=ListActivityUseCase(executions_repo),
        manage_notifications=ManageNotificationsUseCase(notifications_repo),
        check_reminders=CheckRemindersUseCase(
            users_repo, tasks_repo, notifications_repo, _NullEmailSender()
        ),
    )
    client.app.dependency_overrides[get_current_user] = lambda: _USER
    client.app.dependency_overrides[get_request_scope] = lambda: scope
    return {
        "clients_repo": clients_repo,
        "projects_repo": projects_repo,
        "tasks_repo": tasks_repo,
        "thoughts_repo": thoughts_repo,
        "whatsapp_messages_repo": whatsapp_messages_repo,
        "executions_repo": executions_repo,
        "notifications_repo": notifications_repo,
        "calendar_port": calendar_port,
        "drive_port": drive_port,
        "logo_storage": logo_storage,
    }


def test_dashboard_summary_returns_counts_and_live_stats(client: TestClient) -> None:
    _install_scope(client)

    response = client.get("/api/v1/dashboard/summary")

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "open_tasks": 0,
        "active_projects": 0,
        "total_clients": 0,
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


def test_delete_client_removes_it(client: TestClient) -> None:
    _install_scope(client)
    created = client.post("/api/v1/clients", json={"name": "Baron's"}).json()

    response = client.delete(f"/api/v1/clients/{created['id']}")
    assert response.status_code == 204

    list_response = client.get("/api/v1/clients")
    assert list_response.json() == []


def test_delete_client_rejects_other_users_client(client: TestClient) -> None:
    resources = _install_scope(client)
    created = client.post("/api/v1/clients", json={"name": "Baron's"}).json()

    clients_repo = resources["clients_repo"]
    stored = clients_repo.clients[uuid.UUID(created["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.delete(f"/api/v1/clients/{created['id']}")

    assert response.status_code == 403


def test_upload_and_fetch_client_logo(client: TestClient) -> None:
    _install_scope(client)
    created = client.post("/api/v1/clients", json={"name": "Baron's"}).json()
    assert created["has_logo"] is False

    upload_response = client.post(
        f"/api/v1/clients/{created['id']}/logo",
        files={"logo": ("logo.png", b"fake-image-bytes", "image/png")},
    )
    assert upload_response.status_code == 200
    assert upload_response.json()["has_logo"] is True

    logo_response = client.get(f"/api/v1/clients/{created['id']}/logo")
    assert logo_response.status_code == 200
    assert logo_response.content == b"fake-image-bytes"
    assert logo_response.headers["content-type"] == "image/png"


def test_upload_client_logo_rejects_non_image(client: TestClient) -> None:
    _install_scope(client)
    created = client.post("/api/v1/clients", json={"name": "Baron's"}).json()

    response = client.post(
        f"/api/v1/clients/{created['id']}/logo",
        files={"logo": ("notes.txt", b"hello", "text/plain")},
    )

    assert response.status_code == 422


def test_upload_client_logo_rejects_other_users_client(client: TestClient) -> None:
    resources = _install_scope(client)
    created = client.post("/api/v1/clients", json={"name": "Baron's"}).json()

    clients_repo = resources["clients_repo"]
    stored = clients_repo.clients[uuid.UUID(created["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.post(
        f"/api/v1/clients/{created['id']}/logo",
        files={"logo": ("logo.png", b"fake-image-bytes", "image/png")},
    )

    assert response.status_code == 403


def test_create_project_requires_client(client: TestClient) -> None:
    _install_scope(client)

    response = client.post(
        "/api/v1/projects", json={"name": "Summer menu", "type": "consulting"}
    )

    assert response.status_code == 422


def test_create_project_requires_type(client: TestClient) -> None:
    _install_scope(client)
    client_entity = client.post("/api/v1/clients", json={"name": "Baron's"}).json()

    response = client.post(
        "/api/v1/projects", json={"name": "Summer menu", "client_id": client_entity["id"]}
    )

    assert response.status_code == 422


def test_create_and_list_projects(client: TestClient) -> None:
    _install_scope(client)
    client_entity = client.post("/api/v1/clients", json={"name": "Baron's"}).json()

    create_response = client.post(
        "/api/v1/projects",
        json={"name": "Summer menu", "client_id": client_entity["id"], "type": "consulting"},
    )
    assert create_response.status_code == 200
    body = create_response.json()
    assert body["name"] == "Summer menu"
    assert body["type"] == "consulting"
    assert body["client_name"] == "Baron's"

    list_response = client.get("/api/v1/projects")
    assert len(list_response.json()) == 1


def test_update_project_type(client: TestClient) -> None:
    _install_scope(client)
    client_entity = client.post("/api/v1/clients", json={"name": "Baron's"}).json()
    project = client.post(
        "/api/v1/projects",
        json={"name": "Rebrand", "client_id": client_entity["id"], "type": "consulting"},
    ).json()

    response = client.patch(
        f"/api/v1/projects/{project['id']}/type", json={"type": "mentoring"}
    )

    assert response.status_code == 200
    assert response.json()["type"] == "mentoring"


def test_assign_project_client(client: TestClient) -> None:
    _install_scope(client)
    original_client = client.post("/api/v1/clients", json={"name": "Baron's"}).json()
    new_client = client.post("/api/v1/clients", json={"name": "Other Co"}).json()
    project = client.post(
        "/api/v1/projects",
        json={"name": "Rebrand", "client_id": original_client["id"], "type": "consulting"},
    ).json()

    response = client.patch(
        f"/api/v1/projects/{project['id']}/client", json={"client_id": new_client["id"]}
    )

    assert response.status_code == 200
    assert response.json()["client_id"] == new_client["id"]
    assert response.json()["client_name"] == "Other Co"


def test_assign_project_client_rejects_other_users_project(client: TestClient) -> None:
    resources = _install_scope(client)
    client_entity = client.post("/api/v1/clients", json={"name": "Baron's"}).json()
    other_user_project = client.post(
        "/api/v1/projects",
        json={"name": "Not yours", "client_id": client_entity["id"], "type": "consulting"},
    ).json()

    projects_repo = resources["projects_repo"]
    stored = projects_repo.projects[uuid.UUID(other_user_project["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.patch(
        f"/api/v1/projects/{other_user_project['id']}/client",
        json={"client_id": client_entity["id"]},
    )

    assert response.status_code == 403


def test_delete_project_removes_it(client: TestClient) -> None:
    _install_scope(client)
    client_entity = client.post("/api/v1/clients", json={"name": "Baron's"}).json()
    project = client.post(
        "/api/v1/projects",
        json={"name": "Throwaway", "client_id": client_entity["id"], "type": "consulting"},
    ).json()

    response = client.delete(f"/api/v1/projects/{project['id']}")
    assert response.status_code == 204

    list_response = client.get("/api/v1/projects")
    assert list_response.json() == []


def test_delete_project_rejects_other_users_project(client: TestClient) -> None:
    resources = _install_scope(client)
    client_entity = client.post("/api/v1/clients", json={"name": "Baron's"}).json()
    other_user_project = client.post(
        "/api/v1/projects",
        json={"name": "Not yours", "client_id": client_entity["id"], "type": "consulting"},
    ).json()

    projects_repo = resources["projects_repo"]
    stored = projects_repo.projects[uuid.UUID(other_user_project["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.delete(f"/api/v1/projects/{other_user_project['id']}")

    assert response.status_code == 403


def test_update_project_type_rejects_other_users_project(client: TestClient) -> None:
    resources = _install_scope(client)
    client_entity = client.post("/api/v1/clients", json={"name": "Baron's"}).json()
    other_user_project = client.post(
        "/api/v1/projects",
        json={"name": "Not yours", "client_id": client_entity["id"], "type": "consulting"},
    ).json()

    # simulate the project belonging to someone else by mutating the fake repo directly
    projects_repo = resources["projects_repo"]
    stored = projects_repo.projects[uuid.UUID(other_user_project["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.patch(
        f"/api/v1/projects/{other_user_project['id']}/type", json={"type": "setup"}
    )

    assert response.status_code == 403


def test_create_and_toggle_task(client: TestClient) -> None:
    _install_scope(client)
    task = client.post("/api/v1/tasks", json=_task_payload(title="Prep summer menu")).json()
    assert task["status"] == "open"

    response = client.patch(f"/api/v1/tasks/{task['id']}/status", json={"status": "done"})

    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_update_task_status_rejects_other_users_task(client: TestClient) -> None:
    resources = _install_scope(client)
    task = client.post("/api/v1/tasks", json=_task_payload(title="Not yours")).json()

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


def test_create_task_requires_start_at_and_due_at(client: TestClient) -> None:
    _install_scope(client)

    response = client.post("/api/v1/tasks", json={"title": "No times given"})

    assert response.status_code == 422
    assert response.json()["error_code"] == "validation_error"


def test_create_task_requires_start_at_even_with_due_at(client: TestClient) -> None:
    _install_scope(client)

    response = client.post(
        "/api/v1/tasks", json={"title": "Only end time", "due_at": "2026-08-01T09:00:00Z"}
    )

    assert response.status_code == 422


def test_create_task_with_due_at_and_update_details(client: TestClient) -> None:
    _install_scope(client)
    task = client.post(
        "/api/v1/tasks", json=_task_payload(title="Send invoice", due_at="2026-08-01T09:00:00Z")
    ).json()
    assert task["due_at"] is not None

    response = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={"title": "Send invoice", "due_at": "2026-09-01T09:00:00Z"},
    )

    assert response.status_code == 200
    assert response.json()["due_at"].startswith("2026-09-01")


def test_update_task_rejects_other_users_task(client: TestClient) -> None:
    resources = _install_scope(client)
    task = client.post("/api/v1/tasks", json=_task_payload(title="Not yours")).json()

    tasks_repo = resources["tasks_repo"]
    stored = tasks_repo.tasks[uuid.UUID(task["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={"title": "Not yours", "due_at": "2026-09-01T09:00:00Z"},
    )

    assert response.status_code == 403


def test_update_task_can_assign_client_and_clear_project(client: TestClient) -> None:
    resources = _install_scope(client)
    clients_repo = resources["clients_repo"]
    client_entity = client.post("/api/v1/clients", json={"name": "Acme"}).json()
    project = client.post(
        "/api/v1/projects",
        json={"name": "Website", "client_id": client_entity["id"], "type": "consulting"},
    ).json()
    task = client.post(
        "/api/v1/tasks", json=_task_payload(title="Kickoff call", project_id=project["id"])
    ).json()
    assert clients_repo  # sanity: fixture wired, avoids unused-var lint

    response = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={"title": "Kickoff call", "project_id": None, "client_id": client_entity["id"]},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["project_id"] is None
    assert body["client_id"] == client_entity["id"]


def test_delete_task_removes_it(client: TestClient) -> None:
    _install_scope(client)
    task = client.post("/api/v1/tasks", json=_task_payload(title="Throwaway")).json()

    response = client.delete(f"/api/v1/tasks/{task['id']}")
    assert response.status_code == 204

    list_response = client.get("/api/v1/tasks")
    assert list_response.json() == []


def test_delete_task_rejects_other_users_task(client: TestClient) -> None:
    resources = _install_scope(client)
    task = client.post("/api/v1/tasks", json=_task_payload(title="Not yours")).json()

    tasks_repo = resources["tasks_repo"]
    stored = tasks_repo.tasks[uuid.UUID(task["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.delete(f"/api/v1/tasks/{task['id']}")

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


def test_create_and_list_calendar_events(client: TestClient) -> None:
    _install_scope(client)

    create_response = client.post(
        "/api/v1/calendar/events",
        json={
            "summary": "Team sync",
            "start_time": "2026-08-01T09:00:00Z",
            "end_time": "2026-08-01T09:30:00Z",
        },
    )
    assert create_response.status_code == 200
    body = create_response.json()
    assert body["summary"] == "Team sync"

    list_response = client.get("/api/v1/calendar/events")
    assert [e["summary"] for e in list_response.json()] == ["Team sync"]


def test_delete_calendar_event(client: TestClient) -> None:
    resources = _install_scope(client)
    created = client.post(
        "/api/v1/calendar/events",
        json={
            "summary": "One-off",
            "start_time": "2026-08-01T09:00:00Z",
            "end_time": "2026-08-01T09:30:00Z",
        },
    ).json()

    response = client.delete(f"/api/v1/calendar/events/{created['id']}")

    assert response.status_code == 204
    calendar_port: _FakeCalendar = resources["calendar_port"]  # type: ignore[assignment]
    assert created["id"] not in calendar_port.events


def test_create_list_and_share_file(client: TestClient) -> None:
    resources = _install_scope(client)

    create_response = client.post(
        "/api/v1/files", json={"name": "notes.txt", "content": "hello", "mime_type": "text/plain"}
    )
    assert create_response.status_code == 200
    file_id = create_response.json()["id"]
    assert create_response.json()["name"] == "notes.txt"

    list_response = client.get("/api/v1/files")
    assert [f["name"] for f in list_response.json()] == ["notes.txt"]

    content_response = client.get(f"/api/v1/files/{file_id}/content")
    assert content_response.status_code == 200
    assert content_response.json()["content"] == "file content"

    share_response = client.post(
        f"/api/v1/files/{file_id}/share", json={"email": "friend@example.com", "role": "writer"}
    )
    assert share_response.status_code == 204
    drive_port: _FakeDrive = resources["drive_port"]  # type: ignore[assignment]
    assert drive_port.shares == [(file_id, "friend@example.com", "writer")]


def test_create_and_list_thoughts(client: TestClient) -> None:
    _install_scope(client)

    create_response = client.post("/api/v1/thoughts", json={"content": "call the accountant"})
    assert create_response.status_code == 200
    assert create_response.json()["content"] == "call the accountant"

    list_response = client.get("/api/v1/thoughts")
    assert [t["content"] for t in list_response.json()] == ["call the accountant"]


def test_create_thought_rejects_blank_content(client: TestClient) -> None:
    _install_scope(client)

    response = client.post("/api/v1/thoughts", json={"content": "   "})

    assert response.status_code == 422


def test_delete_thought_removes_it(client: TestClient) -> None:
    _install_scope(client)
    thought = client.post("/api/v1/thoughts", json={"content": "Throwaway"}).json()

    response = client.delete(f"/api/v1/thoughts/{thought['id']}")
    assert response.status_code == 204

    list_response = client.get("/api/v1/thoughts")
    assert list_response.json() == []


def test_delete_thought_rejects_other_users_thought(client: TestClient) -> None:
    resources = _install_scope(client)
    thought = client.post("/api/v1/thoughts", json={"content": "Not yours"}).json()

    thoughts_repo = resources["thoughts_repo"]
    stored = thoughts_repo.thoughts[uuid.UUID(thought["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.delete(f"/api/v1/thoughts/{thought['id']}")

    assert response.status_code == 403
