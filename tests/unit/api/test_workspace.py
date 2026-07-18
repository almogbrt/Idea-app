from __future__ import annotations

import uuid
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.application.ports.inbox import InboxPort
from app.application.ports.schedule import SchedulePort
from app.application.use_cases.manage_workspace import (
    DashboardSummaryUseCase,
    ListActivityUseCase,
    ManageClientsUseCase,
    ManageProjectsUseCase,
    ManageTasksUseCase,
)
from app.core.container import RequestScopedServices
from app.domain.entities import User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from tests.conftest import (
    FakeAgentExecutionRepository,
    FakeClientRepository,
    FakeProjectRepository,
    FakeTaskRepository,
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


def _install_scope(client: TestClient) -> dict[str, object]:
    clients_repo = FakeClientRepository()
    projects_repo = FakeProjectRepository()
    tasks_repo = FakeTaskRepository()
    executions_repo = FakeAgentExecutionRepository()

    scope = RequestScopedServices(
        orchestrator=_NullOrchestrator(),  # type: ignore[arg-type]
        manage_conversation=None,  # type: ignore[arg-type]
        authenticate_user=None,  # type: ignore[arg-type]
        manage_clients=ManageClientsUseCase(clients_repo),
        manage_projects=ManageProjectsUseCase(projects_repo),
        manage_tasks=ManageTasksUseCase(tasks_repo),
        dashboard_summary=DashboardSummaryUseCase(
            projects_repo, tasks_repo, _NullInbox(), _NullSchedule()
        ),
        list_activity=ListActivityUseCase(executions_repo),
    )
    client.app.dependency_overrides[get_current_user] = lambda: _USER
    client.app.dependency_overrides[get_request_scope] = lambda: scope
    return {
        "clients_repo": clients_repo,
        "projects_repo": projects_repo,
        "tasks_repo": tasks_repo,
        "executions_repo": executions_repo,
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
