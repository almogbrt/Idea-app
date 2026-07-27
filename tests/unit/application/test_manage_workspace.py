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
    ManageThoughtsUseCase,
    compute_monthly_task_progress,
)
from app.core.exceptions import ExternalServiceError, NotFoundError, ValidationError
from app.domain.entities import (
    AgentExecution,
    EmailSummary,
    ExecutionStatus,
    ProjectType,
    Task,
    TaskCategory,
    TaskStatus,
)
from tests.conftest import (
    FakeAgentExecutionRepository,
    FakeClientAttachmentRepository,
    FakeClientLogoStorage,
    FakeClientRepository,
    FakeProjectRepository,
    FakeTaskRepository,
    FakeThoughtRepository,
)


class _FailingInbox(InboxPort):
    async def count_unread(self, user_id: uuid.UUID) -> int:
        raise ExternalServiceError("Gmail is down")

    async def list_recent(self, user_id: uuid.UUID, max_results: int) -> list[EmailSummary]:
        raise ExternalServiceError("Gmail is down")


class _FailingSchedule(SchedulePort):
    async def count_meetings_today(self, user_id: uuid.UUID) -> int:
        raise ExternalServiceError("Calendar is down")


class _WorkingInbox(InboxPort):
    async def count_unread(self, user_id: uuid.UUID) -> int:
        return 7

    async def list_recent(self, user_id: uuid.UUID, max_results: int) -> list[EmailSummary]:
        return []


class _WorkingSchedule(SchedulePort):
    async def count_meetings_today(self, user_id: uuid.UUID) -> int:
        return 2


async def test_manage_clients_create_and_list(
    fake_client_repository: FakeClientRepository,
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = ManageClientsUseCase(
        fake_client_repository,
        fake_project_repository,
        fake_task_repository,
        FakeClientLogoStorage(),
        FakeClientAttachmentRepository(),
    )
    user_id = uuid.uuid4()

    client = await use_case.create(user_id, "Baron's")
    clients = await use_case.list_all(user_id)

    assert client.name == "Baron's"
    assert [c.name for c in clients] == ["Baron's"]


async def test_manage_clients_update_sets_only_provided_fields(
    fake_client_repository: FakeClientRepository,
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = ManageClientsUseCase(
        fake_client_repository,
        fake_project_repository,
        fake_task_repository,
        FakeClientLogoStorage(),
        FakeClientAttachmentRepository(),
    )
    user_id = uuid.uuid4()
    client = await use_case.create(user_id, "Baron's")

    updated = await use_case.update(client.id, email="baron@example.com", notes="VIP")

    assert updated.name == "Baron's"
    assert updated.email == "baron@example.com"
    assert updated.notes == "VIP"

    fetched = await use_case.get_or_raise(client.id)
    assert fetched.email == "baron@example.com"


async def test_manage_clients_get_or_raise_missing_client_raises(
    fake_client_repository: FakeClientRepository,
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = ManageClientsUseCase(
        fake_client_repository,
        fake_project_repository,
        fake_task_repository,
        FakeClientLogoStorage(),
        FakeClientAttachmentRepository(),
    )

    with pytest.raises(NotFoundError):
        await use_case.get_or_raise(uuid.uuid4())


async def test_manage_clients_get_detail_returns_linked_projects_and_tasks(
    fake_client_repository: FakeClientRepository,
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = ManageClientsUseCase(
        fake_client_repository,
        fake_project_repository,
        fake_task_repository,
        FakeClientLogoStorage(),
        FakeClientAttachmentRepository(),
    )
    user_id = uuid.uuid4()
    client = await use_case.create(user_id, "Baron's")
    other_client = await use_case.create(user_id, "Other Co")

    project = await fake_project_repository.create(user_id, "Summer menu", client_id=client.id)
    await fake_project_repository.create(user_id, "Unrelated", client_id=other_client.id)
    task = await fake_task_repository.create(user_id, "Design menu", project_id=project.id)
    await fake_task_repository.create(user_id, "Unrelated task")

    detail = await use_case.get_detail(user_id, client.id)

    assert detail.client.id == client.id
    assert [s.project.id for s in detail.projects] == [project.id]
    assert [t.id for t in detail.tasks] == [task.id]


async def test_manage_clients_upload_and_get_logo(
    fake_client_repository: FakeClientRepository,
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_logo_storage: FakeClientLogoStorage,
) -> None:
    use_case = ManageClientsUseCase(
        fake_client_repository,
        fake_project_repository,
        fake_task_repository,
        fake_client_logo_storage,
        FakeClientAttachmentRepository(),
    )
    user_id = uuid.uuid4()
    client = await use_case.create(user_id, "Baron's")

    updated = await use_case.upload_logo(
        user_id, client.id, "logo.png", b"fake-image-bytes", "image/png"
    )
    assert updated.logo_file_id is not None

    content, mime_type = await use_case.get_logo(user_id, client.id)
    assert content == b"fake-image-bytes"
    assert mime_type == "image/png"


async def test_manage_clients_get_logo_raises_when_none_set(
    fake_client_repository: FakeClientRepository,
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_logo_storage: FakeClientLogoStorage,
) -> None:
    use_case = ManageClientsUseCase(
        fake_client_repository,
        fake_project_repository,
        fake_task_repository,
        fake_client_logo_storage,
        FakeClientAttachmentRepository(),
    )
    user_id = uuid.uuid4()
    client = await use_case.create(user_id, "Baron's")

    with pytest.raises(NotFoundError):
        await use_case.get_logo(user_id, client.id)


async def test_manage_clients_upload_list_and_download_attachment(
    fake_client_repository: FakeClientRepository,
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_logo_storage: FakeClientLogoStorage,
    fake_client_attachment_repository: FakeClientAttachmentRepository,
) -> None:
    use_case = ManageClientsUseCase(
        fake_client_repository,
        fake_project_repository,
        fake_task_repository,
        fake_client_logo_storage,
        fake_client_attachment_repository,
    )
    user_id = uuid.uuid4()
    client = await use_case.create(user_id, "Baron's")

    attachment = await use_case.upload_attachment(
        user_id, client.id, "contract.pdf", b"fake-pdf-bytes", "application/pdf"
    )
    assert attachment.filename == "contract.pdf"

    detail = await use_case.get_detail(user_id, client.id)
    assert [a.id for a in detail.attachments] == [attachment.id]

    content, mime_type, filename = await use_case.download_attachment(
        user_id, client.id, attachment.id
    )
    assert content == b"fake-pdf-bytes"
    assert mime_type == "application/pdf"
    assert filename == "contract.pdf"


async def test_manage_clients_delete_attachment_removes_it(
    fake_client_repository: FakeClientRepository,
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_logo_storage: FakeClientLogoStorage,
    fake_client_attachment_repository: FakeClientAttachmentRepository,
) -> None:
    use_case = ManageClientsUseCase(
        fake_client_repository,
        fake_project_repository,
        fake_task_repository,
        fake_client_logo_storage,
        fake_client_attachment_repository,
    )
    user_id = uuid.uuid4()
    client = await use_case.create(user_id, "Baron's")
    attachment = await use_case.upload_attachment(
        user_id, client.id, "contract.pdf", b"fake-pdf-bytes", "application/pdf"
    )

    await use_case.delete_attachment(user_id, client.id, attachment.id)

    detail = await use_case.get_detail(user_id, client.id)
    assert detail.attachments == []
    with pytest.raises(KeyError):
        await fake_client_logo_storage.download(user_id, attachment.file_id)


async def test_manage_clients_download_attachment_from_wrong_client_raises(
    fake_client_repository: FakeClientRepository,
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_logo_storage: FakeClientLogoStorage,
    fake_client_attachment_repository: FakeClientAttachmentRepository,
) -> None:
    use_case = ManageClientsUseCase(
        fake_client_repository,
        fake_project_repository,
        fake_task_repository,
        fake_client_logo_storage,
        fake_client_attachment_repository,
    )
    user_id = uuid.uuid4()
    client = await use_case.create(user_id, "Baron's")
    other_client = await use_case.create(user_id, "Other Co")
    attachment = await use_case.upload_attachment(
        user_id, client.id, "contract.pdf", b"fake-pdf-bytes", "application/pdf"
    )

    with pytest.raises(NotFoundError):
        await use_case.download_attachment(user_id, other_client.id, attachment.id)


async def test_manage_projects_create_list_and_update_type(
    fake_project_repository: FakeProjectRepository,
    fake_client_repository: FakeClientRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    user_id = uuid.uuid4()
    client = await fake_client_repository.create(user_id, "Summer Bistro")

    project = await use_case.create(user_id, "Summer menu", client.id, ProjectType.CONSULTING)
    summaries = await use_case.list_all(user_id)

    assert summaries[0].project.id == project.id
    assert summaries[0].project.type == ProjectType.CONSULTING

    updated = await use_case.update_type(project.id, ProjectType.MENTORING)
    assert updated.type == ProjectType.MENTORING


async def test_manage_projects_create_requires_client(
    fake_project_repository: FakeProjectRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    with pytest.raises(ValidationError):
        await use_case.create(uuid.uuid4(), "Summer menu", type=ProjectType.CONSULTING)


async def test_manage_projects_create_requires_type(
    fake_project_repository: FakeProjectRepository,
    fake_client_repository: FakeClientRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    user_id = uuid.uuid4()
    client = await fake_client_repository.create(user_id, "Summer Bistro")
    with pytest.raises(ValidationError):
        await use_case.create(user_id, "Summer menu", client.id)


async def test_manage_projects_get_or_raise_missing(
    fake_project_repository: FakeProjectRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    with pytest.raises(NotFoundError):
        await use_case.get_or_raise(uuid.uuid4())


async def test_manage_projects_get_summary_or_raise(
    fake_project_repository: FakeProjectRepository,
    fake_client_repository: FakeClientRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    user_id = uuid.uuid4()
    client = await fake_client_repository.create(user_id, "Rebrand Co")
    project = await use_case.create(user_id, "Rebrand", client.id, ProjectType.CONSULTING)

    summary = await use_case.get_summary_or_raise(project.id)
    assert summary.project.id == project.id

    with pytest.raises(NotFoundError):
        await use_case.get_summary_or_raise(uuid.uuid4())


async def test_manage_projects_delete(
    fake_project_repository: FakeProjectRepository,
    fake_client_repository: FakeClientRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    user_id = uuid.uuid4()
    client = await fake_client_repository.create(user_id, "Baron's")
    project = await use_case.create(user_id, "Rebrand", client.id, ProjectType.CONSULTING)

    await use_case.delete(project.id)

    with pytest.raises(NotFoundError):
        await use_case.get_or_raise(project.id)


async def test_manage_projects_assign_client(
    fake_project_repository: FakeProjectRepository,
    fake_client_repository: FakeClientRepository,
) -> None:
    use_case = ManageProjectsUseCase(fake_project_repository)
    user_id = uuid.uuid4()
    original_client = await fake_client_repository.create(user_id, "Old Client")
    new_client = await fake_client_repository.create(user_id, "New Client")
    project = await use_case.create(user_id, "Rebrand", original_client.id, ProjectType.CONSULTING)

    updated = await use_case.assign_client(project.id, new_client.id)

    assert updated.client_id == new_client.id


async def test_manage_tasks_create_list_and_update_status(
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = ManageTasksUseCase(fake_task_repository)
    user_id = uuid.uuid4()

    start = datetime(2026, 8, 1, 8, 0, tzinfo=UTC)
    due = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)
    task = await use_case.create(
        user_id, "Prep summer menu", due_at=due, start_at=start, category=TaskCategory.OPERATIONAL
    )
    tasks = await use_case.list_all(user_id)

    assert tasks[0].id == task.id
    assert tasks[0].status == TaskStatus.OPEN
    assert tasks[0].category == TaskCategory.OPERATIONAL

    updated = await use_case.update_status(task.id, TaskStatus.DONE)
    assert updated.status == TaskStatus.DONE


async def test_manage_tasks_create_rejects_missing_category(
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = ManageTasksUseCase(fake_task_repository)
    user_id = uuid.uuid4()
    start = datetime(2026, 8, 1, 8, 0, tzinfo=UTC)
    due = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)

    with pytest.raises(ValidationError):
        await use_case.create(user_id, "Prep summer menu", due_at=due, start_at=start)


def _progress_task(
    *, due_at: datetime | None, completed_at: datetime | None = None
) -> Task:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    return Task(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        project_id=None,
        title="t",
        status=TaskStatus.DONE if completed_at else TaskStatus.OPEN,
        created_at=now,
        updated_at=now,
        due_at=due_at,
        completed_at=completed_at,
    )


def test_compute_monthly_task_progress_rolls_over_unfinished_tasks() -> None:
    today = datetime(2026, 7, 15, 12, 0, tzinfo=UTC)

    due_this_month_completed_day5 = _progress_task(
        due_at=datetime(2026, 7, 10, tzinfo=UTC),
        completed_at=datetime(2026, 7, 5, 9, 0, tzinfo=UTC),
    )
    overdue_from_last_month_still_open = _progress_task(
        due_at=datetime(2026, 6, 20, tzinfo=UTC)
    )
    finished_last_month_does_not_roll_over = _progress_task(
        due_at=datetime(2026, 6, 5, tzinfo=UTC), completed_at=datetime(2026, 6, 6, tzinfo=UTC)
    )
    due_next_month_not_yet_relevant = _progress_task(due_at=datetime(2026, 8, 1, tzinfo=UTC))
    no_due_date_excluded = _progress_task(due_at=None)

    progress = compute_monthly_task_progress(
        [
            due_this_month_completed_day5,
            overdue_from_last_month_still_open,
            finished_last_month_does_not_roll_over,
            due_next_month_not_yet_relevant,
            no_due_date_excluded,
        ],
        today,
    )

    assert progress.month == "2026-07"
    assert progress.today_day == 15
    # Only the two tasks that still "belong" to July count: the one due (and
    # done) in July, and the still-open one rolled over from June.
    assert progress.total_tasks == 2
    assert len(progress.daily_completed) == 15
    assert progress.daily_completed[3] == 0  # day 4: not completed yet
    assert progress.daily_completed[4] == 1  # day 5: the completed task counts
    assert progress.daily_completed[14] == 1  # day 15: still just the one


async def test_quick_capture_creates_task_without_schedule(
    fake_task_repository: FakeTaskRepository,
) -> None:
    """The whole point of quick_capture: unlike create(), it must NOT
    require start_at/due_at — that's what makes it a fast Inbox capture."""
    use_case = ManageTasksUseCase(fake_task_repository)
    user_id = uuid.uuid4()

    task = await use_case.quick_capture(user_id, "  Call the accountant  ")

    assert task.title == "Call the accountant"
    assert task.start_at is None
    assert task.due_at is None
    assert task.status == TaskStatus.OPEN


async def test_quick_capture_rejects_blank_title(
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = ManageTasksUseCase(fake_task_repository)

    with pytest.raises(ValidationError):
        await use_case.quick_capture(uuid.uuid4(), "   ")


async def test_set_next_step(fake_task_repository: FakeTaskRepository) -> None:
    use_case = ManageTasksUseCase(fake_task_repository)
    task = await fake_task_repository.create(uuid.uuid4(), "Write proposal")

    updated = await use_case.set_next_step(task.id, "Send the draft")

    assert updated.next_step == "Send the draft"


async def test_dashboard_summary_aggregates_counts(
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_repository: FakeClientRepository,
) -> None:
    user_id = uuid.uuid4()
    await fake_project_repository.create(user_id, "Consulting project", None)
    await fake_project_repository.create(user_id, "Setup project", None, type=ProjectType.SETUP)
    await fake_task_repository.create(user_id, "Open task")
    done_task = await fake_task_repository.create(user_id, "Done task")
    await fake_task_repository.update_status(done_task.id, TaskStatus.DONE)
    await fake_client_repository.create(user_id, "Client A")

    use_case = DashboardSummaryUseCase(
        fake_project_repository,
        fake_task_repository,
        fake_client_repository,
        _WorkingInbox(),
        _WorkingSchedule(),
    )
    summary = await use_case.execute(user_id)

    assert summary.active_projects == 2
    assert summary.open_tasks == 1
    assert summary.total_clients == 1
    assert summary.unread_emails == 7
    assert summary.meetings_today == 2


async def test_dashboard_summary_degrades_gracefully_when_google_unavailable(
    fake_project_repository: FakeProjectRepository,
    fake_task_repository: FakeTaskRepository,
    fake_client_repository: FakeClientRepository,
) -> None:
    user_id = uuid.uuid4()
    use_case = DashboardSummaryUseCase(
        fake_project_repository,
        fake_task_repository,
        fake_client_repository,
        _FailingInbox(),
        _FailingSchedule(),
    )

    summary = await use_case.execute(user_id)

    assert summary.open_tasks == 0
    assert summary.active_projects == 0
    assert summary.total_clients == 0
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


async def test_manage_thoughts_create_and_list(
    fake_thought_repository: FakeThoughtRepository,
) -> None:
    user_id = uuid.uuid4()
    use_case = ManageThoughtsUseCase(fake_thought_repository)

    thought = await use_case.create(user_id, "  call the accountant tomorrow  ")

    assert thought.content == "call the accountant tomorrow"
    results = await use_case.list_all(user_id)
    assert results == [thought]


async def test_manage_thoughts_create_rejects_blank_content(
    fake_thought_repository: FakeThoughtRepository,
) -> None:
    use_case = ManageThoughtsUseCase(fake_thought_repository)

    with pytest.raises(ValidationError):
        await use_case.create(uuid.uuid4(), "   ")


async def test_manage_thoughts_get_or_raise_not_found(
    fake_thought_repository: FakeThoughtRepository,
) -> None:
    use_case = ManageThoughtsUseCase(fake_thought_repository)

    with pytest.raises(NotFoundError):
        await use_case.get_or_raise(uuid.uuid4())


async def test_manage_thoughts_delete(
    fake_thought_repository: FakeThoughtRepository,
) -> None:
    use_case = ManageThoughtsUseCase(fake_thought_repository)
    thought = await use_case.create(uuid.uuid4(), "an idea")

    await use_case.delete(thought.id)

    assert await use_case.list_all(thought.user_id) == []
