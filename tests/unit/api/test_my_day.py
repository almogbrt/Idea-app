from __future__ import annotations

import uuid
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.application.use_cases.manage_daily_plan import (
    DailyPlanMetricsUseCase,
    ManageDailyPlanUseCase,
    ManageFocusSessionUseCase,
    ManageGoalsUseCase,
)
from app.application.use_cases.manage_workspace import ManageTasksUseCase
from app.core.container import RequestScopedServices
from app.domain.entities import User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from tests.conftest import (
    FakeDailyPlanRepository,
    FakeDailyPlanSwapRepository,
    FakeFocusSessionRepository,
    FakeGoalRepository,
    FakeTaskRepository,
)

_USER = User(
    id=uuid.uuid4(),
    google_sub="sub-my-day",
    email="owner@example.com",
    name="Owner",
    created_at=datetime.now(UTC),
)


def _install_scope(client: TestClient) -> dict[str, object]:
    goals_repo = FakeGoalRepository()
    plans_repo = FakeDailyPlanRepository()
    swaps_repo = FakeDailyPlanSwapRepository()
    sessions_repo = FakeFocusSessionRepository()
    tasks_repo = FakeTaskRepository()

    scope = RequestScopedServices(
        orchestrator=None,  # type: ignore[arg-type]
        manage_conversation=None,  # type: ignore[arg-type]
        authenticate_user=None,  # type: ignore[arg-type]
        manage_clients=None,  # type: ignore[arg-type]
        manage_projects=None,  # type: ignore[arg-type]
        manage_tasks=ManageTasksUseCase(tasks_repo),
        manage_thoughts=None,  # type: ignore[arg-type]
        manage_whatsapp_messages=None,  # type: ignore[arg-type]
        dashboard_summary=None,  # type: ignore[arg-type]
        list_activity=None,  # type: ignore[arg-type]
        manage_notifications=None,  # type: ignore[arg-type]
        check_reminders=None,  # type: ignore[arg-type]
        send_daily_review=None,  # type: ignore[arg-type]
        manage_calendar=None,  # type: ignore[arg-type]
        manage_email=None,  # type: ignore[arg-type]
        manage_files=None,  # type: ignore[arg-type]
        manage_goals=ManageGoalsUseCase(goals_repo),
        manage_daily_plan=ManageDailyPlanUseCase(plans_repo, swaps_repo, tasks_repo),
        manage_focus_sessions=ManageFocusSessionUseCase(sessions_repo, plans_repo),
        daily_plan_metrics=DailyPlanMetricsUseCase(
            plans_repo, sessions_repo, swaps_repo, tasks_repo
        ),
        finance_overview=None,  # type: ignore[arg-type]
    )
    client.app.dependency_overrides[get_current_user] = lambda: _USER
    client.app.dependency_overrides[get_request_scope] = lambda: scope
    return {
        "goals_repo": goals_repo,
        "plans_repo": plans_repo,
        "swaps_repo": swaps_repo,
        "sessions_repo": sessions_repo,
        "tasks_repo": tasks_repo,
    }


def _pick_payload(task_id: str, **overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "task_id": task_id,
        "deliverable": "A finished draft",
        "estimated_minutes": 60,
        "importance": "high",
        "goal_id": None,
        "next_step": "Open the draft and write one sentence",
    }
    payload.update(overrides)
    return payload


def test_create_list_update_delete_goal(client: TestClient) -> None:
    _install_scope(client)

    created = client.post("/api/v1/my-day/goals", json={"name": "Grow the business"}).json()
    assert created["name"] == "Grow the business"

    listed = client.get("/api/v1/my-day/goals").json()
    assert [g["name"] for g in listed] == ["Grow the business"]

    updated = client.patch(
        f"/api/v1/my-day/goals/{created['id']}", json={"name": "Grow 2x"}
    ).json()
    assert updated["name"] == "Grow 2x"

    delete_response = client.delete(f"/api/v1/my-day/goals/{created['id']}")
    assert delete_response.status_code == 204
    assert client.get("/api/v1/my-day/goals").json() == []


def test_goal_endpoints_reject_other_users_goal(client: TestClient) -> None:
    resources = _install_scope(client)
    created = client.post("/api/v1/my-day/goals", json={"name": "Grow"}).json()

    goals_repo = resources["goals_repo"]
    stored = goals_repo.goals[uuid.UUID(created["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    patch_response = client.patch(f"/api/v1/my-day/goals/{created['id']}", json={"name": "x"})
    assert patch_response.status_code == 403
    delete_response = client.delete(f"/api/v1/my-day/goals/{created['id']}")
    assert delete_response.status_code == 403


def test_quick_capture_creates_unscheduled_task(client: TestClient) -> None:
    _install_scope(client)

    response = client.post("/api/v1/my-day/inbox", json={"title": "Call the accountant"})

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Call the accountant"
    assert body["start_at"] is None
    assert body["due_at"] is None


def test_get_today_plan_creates_one_if_missing(client: TestClient) -> None:
    _install_scope(client)

    response = client.get("/api/v1/my-day/plan/today")

    assert response.status_code == 200
    assert response.json()["is_locked"] is False


def test_select_lock_and_start_focus_flow(client: TestClient) -> None:
    _install_scope(client)
    main_task = client.post("/api/v1/my-day/inbox", json={"title": "Main task"}).json()

    select_response = client.post(
        "/api/v1/my-day/plan/today/select",
        json={"main": _pick_payload(main_task["id"]), "secondary": []},
    )
    assert select_response.status_code == 200
    assert select_response.json()["main_task_id"] == main_task["id"]

    lock_response = client.post("/api/v1/my-day/plan/today/lock")
    assert lock_response.status_code == 200
    assert lock_response.json()["is_locked"] is True

    start_response = client.post("/api/v1/my-day/focus/start", json={"task_id": main_task["id"]})
    assert start_response.status_code == 200
    session = start_response.json()
    assert session["ended_at"] is None

    active_response = client.get("/api/v1/my-day/focus/active")
    assert active_response.json()["id"] == session["id"]

    end_response = client.post(
        f"/api/v1/my-day/focus/{session['id']}/end", json={"exit_reason": "done"}
    )
    assert end_response.status_code == 200
    assert end_response.json()["exit_reason"] == "done"

    tasks = client.get("/api/v1/tasks").json()
    updated_task = next(t for t in tasks if t["id"] == main_task["id"])
    assert updated_task["status"] == "done"

    assert client.get("/api/v1/my-day/focus/active").json() is None


def test_end_focus_stuck_requires_stuck_reason(client: TestClient) -> None:
    _install_scope(client)
    main_task = client.post("/api/v1/my-day/inbox", json={"title": "Main task"}).json()
    client.post(
        "/api/v1/my-day/plan/today/select",
        json={"main": _pick_payload(main_task["id"]), "secondary": []},
    )
    client.post("/api/v1/my-day/plan/today/lock")
    session = client.post(
        "/api/v1/my-day/focus/start", json={"task_id": main_task["id"]}
    ).json()

    response = client.post(
        f"/api/v1/my-day/focus/{session['id']}/end", json={"exit_reason": "stuck"}
    )

    assert response.status_code == 422


def test_end_focus_rejects_other_users_session(client: TestClient) -> None:
    resources = _install_scope(client)
    main_task = client.post("/api/v1/my-day/inbox", json={"title": "Main task"}).json()
    client.post(
        "/api/v1/my-day/plan/today/select",
        json={"main": _pick_payload(main_task["id"]), "secondary": []},
    )
    client.post("/api/v1/my-day/plan/today/lock")
    session = client.post(
        "/api/v1/my-day/focus/start", json={"task_id": main_task["id"]}
    ).json()

    sessions_repo = resources["sessions_repo"]
    stored = sessions_repo.sessions[uuid.UUID(session["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.post(
        f"/api/v1/my-day/focus/{session['id']}/end", json={"exit_reason": "done"}
    )
    assert response.status_code == 403


def test_start_focus_requires_locked_plan(client: TestClient) -> None:
    _install_scope(client)
    task = client.post("/api/v1/my-day/inbox", json={"title": "Task"}).json()

    response = client.post("/api/v1/my-day/focus/start", json={"task_id": task["id"]})

    assert response.status_code == 422


def test_swap_daily_task(client: TestClient) -> None:
    _install_scope(client)
    main_task = client.post("/api/v1/my-day/inbox", json={"title": "Main task"}).json()
    secondary_task = client.post("/api/v1/my-day/inbox", json={"title": "Secondary task"}).json()
    urgent_task = client.post("/api/v1/my-day/inbox", json={"title": "Urgent task"}).json()
    client.post(
        "/api/v1/my-day/plan/today/select",
        json={
            "main": _pick_payload(main_task["id"]),
            "secondary": [_pick_payload(secondary_task["id"])],
        },
    )
    client.post("/api/v1/my-day/plan/today/lock")

    response = client.post(
        "/api/v1/my-day/plan/today/swap",
        json={
            "bumped_task_id": secondary_task["id"],
            "pick": _pick_payload(urgent_task["id"]),
        },
    )

    assert response.status_code == 200
    assert response.json()["secondary_task_id_1"] == urgent_task["id"]


def test_plan_tomorrows_first_task(client: TestClient) -> None:
    _install_scope(client)
    task = client.post("/api/v1/my-day/inbox", json={"title": "Tomorrow's task"}).json()

    response = client.post(
        "/api/v1/my-day/plan/tomorrow/first-task", json=_pick_payload(task["id"])
    )

    assert response.status_code == 200
    body = response.json()
    assert body["main_task_id"] == task["id"]
    assert body["is_locked"] is True

    today = client.get("/api/v1/my-day/plan/today").json()
    assert today["carry_over_task_id"] == task["id"]


def test_plan_tomorrows_first_task_rejects_if_already_locked(client: TestClient) -> None:
    _install_scope(client)
    task = client.post("/api/v1/my-day/inbox", json={"title": "Tomorrow's task"}).json()
    other_task = client.post("/api/v1/my-day/inbox", json={"title": "Another task"}).json()
    client.post("/api/v1/my-day/plan/tomorrow/first-task", json=_pick_payload(task["id"]))

    response = client.post(
        "/api/v1/my-day/plan/tomorrow/first-task", json=_pick_payload(other_task["id"])
    )

    assert response.status_code == 409


def test_end_of_day_summary(client: TestClient) -> None:
    _install_scope(client)
    main_task = client.post("/api/v1/my-day/inbox", json={"title": "Main task"}).json()
    client.post(
        "/api/v1/my-day/plan/today/select",
        json={"main": _pick_payload(main_task["id"]), "secondary": []},
    )
    client.post("/api/v1/my-day/plan/today/lock")
    session = client.post(
        "/api/v1/my-day/focus/start", json={"task_id": main_task["id"]}
    ).json()
    client.post(f"/api/v1/my-day/focus/{session['id']}/end", json={"exit_reason": "done"})

    response = client.get("/api/v1/my-day/plan/today/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["main_task_completed"] is True
    assert body["completed_tasks"] == ["Main task"]


def test_metrics(client: TestClient) -> None:
    _install_scope(client)
    main_task = client.post("/api/v1/my-day/inbox", json={"title": "Main task"}).json()
    client.post(
        "/api/v1/my-day/plan/today/select",
        json={"main": _pick_payload(main_task["id"]), "secondary": []},
    )
    client.post("/api/v1/my-day/plan/today/lock")
    session = client.post(
        "/api/v1/my-day/focus/start", json={"task_id": main_task["id"]}
    ).json()
    client.post(f"/api/v1/my-day/focus/{session['id']}/end", json={"exit_reason": "done"})

    response = client.get(
        "/api/v1/my-day/metrics?from_date=2020-01-01&to_date=2030-01-01"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["main_task_completion_rate"] == 1.0
    assert body["focus_blocks_completed"] == 1


def test_set_task_next_step(client: TestClient) -> None:
    _install_scope(client)
    task = client.post("/api/v1/my-day/inbox", json={"title": "Write proposal"}).json()

    response = client.patch(
        f"/api/v1/my-day/tasks/{task['id']}/next-step", json={"next_step": "Send the draft"}
    )

    assert response.status_code == 200
    assert response.json()["next_step"] == "Send the draft"


def test_set_task_next_step_rejects_other_users_task(client: TestClient) -> None:
    resources = _install_scope(client)
    task = client.post("/api/v1/my-day/inbox", json={"title": "Not yours"}).json()

    tasks_repo = resources["tasks_repo"]
    stored = tasks_repo.tasks[uuid.UUID(task["id"])]  # type: ignore[attr-defined]
    stored.user_id = uuid.uuid4()

    response = client.patch(
        f"/api/v1/my-day/tasks/{task['id']}/next-step", json={"next_step": "x"}
    )
    assert response.status_code == 403


def test_my_day_endpoints_require_authentication(client: TestClient) -> None:
    response = client.get("/api/v1/my-day/plan/today")
    assert response.status_code == 401
