from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from app.application.ports.inbox import InboxPort
from app.application.ports.schedule import SchedulePort
from app.application.use_cases.manage_workspace import (
    DashboardSummaryUseCase,
    ListActivityUseCase,
    ManageClientsUseCase,
    ManageProjectsUseCase,
    ManageTasksUseCase,
)
from app.core.exceptions import ExternalServiceError, NotFoundError
from app.domain.entities import (
    AgentExecution,
    ExecutionStatus,
    ProjectStatus,
    TaskStatus,
)
from tests.conftest import (
    FakeAgentExecutionRepository,
    FakeClientRepository,
    FakeProjectRepository,
    FakeTaskRepository,
)


class _FailingInbox(InboxPort):
    async def count_unread(self, user_id: uuid.UUID) -> int:
        raise ExternalServiceError("Gmail is down")


class _FailingSchedule(SchedulePort):
    async def count_meetings_today(self, user_id: uuid.UUID) -> int:
        raise ExternalServiceError("Calendar is down")


class _WorkingInbox(InboxPort):
    async def count_unread(self, user_id: uuid.UUID) -> int:
        return 7


class _WorkingSchedule(SchedulePort):
    async def count_meetings_today(self, user_id: uuid.UUID) -> int:
        return 2


async def test_manage_clients_create_and_list(fake_client_repository: FakeClientRepository) -> None:
    use_case = ManageClientsUseCase(fake_client_repository)
    user_id = uuid.uuid4()

    client = await use_case.create(user_id, "Baron's")
    clients = await use_case.list_all(user_id)

    assert client.name == "Baron's"
    assert [c.name for c in clients] == ["Baron's"]


async def test_manage_projects_create_list_and_update_status(
    fake_project_repository: FakeProjectRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    user_id = uuid.uuid4()

    project = await use_case.create(user_id, "Summer menu")
    summaries = await use_case.list_all(user_id)

    assert summaries[0].project.id == project.id
    assert summaries[0].project.status == ProjectStatus.IN_PROGRESS

    updated = await use_case.update_status(project.id, ProjectStatus.ON_HOLD)
    assert updated.status == ProjectStatus.ON_HOLD


async def test_manage_projects_get_or_raise_missing(
    fake_project_repository: FakeProjectRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    with pytest.raises(NotFoundError):
        await use_case.get_or_raise(uuid.uuid4())


async def test_manage_projects_get_summary_or_raise(
    fake_project_repository: FakeProjectRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    user_id = uuid.uuid4()
    project = await use_case.create(user_id, "Rebrand")

    summary = await use_case.get_summary_or_raise(project.id)
    assert summary.project.id == project.id

    with pytest.raises(NotFoundError):
        await use_case.get_summary_or_raise(uuid.uuid4())


async def test_manage_tasks_create_list_and_update_status(
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = ManageTasksUseCase(fake_task_repository)
    user_id = uuid.uuid4()

    task = await use_case.create(user_id, "Prep summer menu")
    tasks = await use_case.list_all(user_id)

    assert tasks[0].id == task.id
    assert tasks[0].status == TaskStatus.OPEN

    updated = await use_case.update_status(task.id, TaskStatus.DONE)
    assert updated.status == TaskStatus.DONE


async def test_dashboard_summary_aggregates_counts(
    fake_project_repository: FakeProjectRepository, fake_task_repository: FakeTaskRepository
) -> None:
    user_id = uuid.uuid4()
    await fake_project_repository.create(user_id, "Active project")
    await fake_project_repository.create(
        user_id, "On hold project", status=ProjectStatus.ON_HOLD
    )
    await fake_task_repository.create(user_id, "Open task")
    done_task = await fake_task_repository.create(user_id, "Done task")
    await fake_task_repository.update_status(done_task.id, TaskStatus.DONE)

    use_case = DashboardSummaryUseCase(
        fake_project_repository, fake_task_repository, _WorkingInbox(), _WorkingSchedule()
    )
    summary = await use_case.execute(user_id)

    assert summary.active_projects == 1
    assert summary.open_tasks == 1
    assert summary.unread_emails == 7
    assert summary.meetings_today == 2


async def test_dashboard_summary_degrades_gracefully_when_google_unavailable(
    fake_project_repository: FakeProjectRepository, fake_task_repository: FakeTaskRepository
) -> None:
    user_id = uuid.uuid4()
    use_case = DashboardSummaryUseCase(
        fake_project_repository, fake_task_repository, _FailingInbox(), _FailingSchedule()
    )

    summary = await use_case.execute(user_id)

    assert summary.open_tasks == 0
    assert summary.active_projects == 0
    assert summary.unread_emails is None
    assert summary.meetings_today is None


async def test_list_activity_returns_only_requesting_users_executions(
    fake_agent_execution_repository: FakeAgentExecutionRepository,
) -> None:
    user_id = uuid.uuid4()
    other_user_id = uuid.uuid4()

    await fake_agent_execution_repository.record(
        AgentExecution(
            id=uuid.uuid4(),
            user_id=user_id,
            agent_name="gmail",
            tool_name="gmail_send_email",
            input={},
            output={},
            status=ExecutionStatus.SUCCESS,
            latency_ms=10,
            created_at=datetime.now(UTC),
        )
    )
    await fake_agent_execution_repository.record(
        AgentExecution(
            id=uuid.uuid4(),
            user_id=other_user_id,
            agent_name="gmail",
            tool_name="gmail_send_email",
            input={},
            output={},
            status=ExecutionStatus.SUCCESS,
            latency_ms=10,
            created_at=datetime.now(UTC),
        )
    )

    use_case = ListActivityUseCase(fake_agent_execution_repository)
    results = await use_case.list_recent(user_id)

    assert len(results) == 1
    assert results[0].user_id == user_id
