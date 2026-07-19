"""Integration tests for `WorkspaceService`'s name-resolution logic.

This is the one piece of custom logic in the `project_management` Agent —
finding a client/project/task by a case-insensitive partial name match, as
an LLM would refer to them in natural language — so it's worth exercising
against a real database rather than only the fakes.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.project_management.service import WorkspaceService
from app.core.exceptions import NotFoundError
from app.domain.entities import ProjectStatus, TaskStatus
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from tests.integration.conftest import TEST_DATABASE_URL, requires_postgres

pytestmark = requires_postgres


@pytest.fixture
def workspace_service() -> WorkspaceService:
    from app.infrastructure.db.session import create_engine, create_session_factory

    engine = create_engine(TEST_DATABASE_URL)
    return WorkspaceService(session_factory=create_session_factory(engine))


async def test_create_project_auto_creates_client_by_name(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-1", "owner-ws1@example.com", "Owner")
    await db_session.commit()

    project = await workspace_service.create_project(user.id, "Summer menu", "Baron's")

    assert project.client_id is not None
    summaries = await workspace_service.list_projects(user.id)
    assert summaries[0].client_name == "Baron's"


async def test_create_project_reuses_existing_client_on_partial_match(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-2", "owner-ws2@example.com", "Owner")
    await db_session.commit()

    first = await workspace_service.create_client(user.id, "Baron's Wine House")
    project = await workspace_service.create_project(user.id, "Rebrand", "baron's")

    assert project.client_id == first.id


async def test_update_project_status_resolves_by_partial_name(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-3", "owner-ws3@example.com", "Owner")
    await db_session.commit()

    await workspace_service.create_project(user.id, "Q3 Marketing Campaign")

    updated = await workspace_service.update_project_status(
        user.id, "marketing", ProjectStatus.ON_HOLD
    )

    assert updated.status == ProjectStatus.ON_HOLD


async def test_update_project_status_raises_when_no_match(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-4", "owner-ws4@example.com", "Owner")
    await db_session.commit()

    with pytest.raises(NotFoundError):
        await workspace_service.update_project_status(
            user.id, "nonexistent project", ProjectStatus.DONE
        )


async def test_create_task_resolves_project_by_partial_name(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-5", "owner-ws5@example.com", "Owner")
    await db_session.commit()

    project = await workspace_service.create_project(user.id, "Summer menu")
    task = await workspace_service.create_task(user.id, "Prep dishes", "summer")

    assert task.project_id == project.id


async def test_update_task_status_resolves_by_partial_title(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-6", "owner-ws6@example.com", "Owner")
    await db_session.commit()

    await workspace_service.create_task(user.id, "Prep the summer menu dishes")

    updated = await workspace_service.update_task_status(
        user.id, "summer menu", TaskStatus.DONE
    )

    assert updated.status == TaskStatus.DONE


async def test_create_task_with_due_at_and_set_task_due_at_resolves_by_partial_title(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-10", "owner-ws10@example.com", "Owner")
    await db_session.commit()

    due = datetime(2026, 8, 1, 9, 0, tzinfo=UTC)
    task = await workspace_service.create_task(user.id, "Send invoice", due_at=due)
    assert task.due_at == due

    new_due = datetime(2026, 9, 1, 9, 0, tzinfo=UTC)
    updated = await workspace_service.set_task_due_at(user.id, "invoice", new_due)

    assert updated.id == task.id
    assert updated.due_at == new_due


async def test_update_client_resolves_by_partial_name_and_sets_only_given_fields(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-7", "owner-ws7@example.com", "Owner")
    await db_session.commit()

    await workspace_service.create_client(user.id, "Baron's Wine House")

    updated = await workspace_service.update_client(
        user.id, "baron's", email="baron@example.com", notes="VIP client"
    )

    assert updated.email == "baron@example.com"
    assert updated.notes == "VIP client"
    assert updated.name == "Baron's Wine House"


async def test_update_client_raises_when_no_match(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-8", "owner-ws8@example.com", "Owner")
    await db_session.commit()

    with pytest.raises(NotFoundError):
        await workspace_service.update_client(user.id, "nonexistent", email="x@example.com")


async def test_delete_task_removes_it(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-11", "owner-ws11@example.com", "Owner")
    await db_session.commit()

    await workspace_service.create_task(user.id, "Throwaway task")
    await workspace_service.delete_task(user.id, "throwaway")

    remaining = await workspace_service.list_tasks(user.id)
    assert remaining == []


async def test_assign_task_client_links_and_clears(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-12", "owner-ws12@example.com", "Owner")
    await db_session.commit()

    client = await workspace_service.create_client(user.id, "Baron's")
    await workspace_service.create_task(user.id, "Kickoff call")

    linked = await workspace_service.assign_task_client(user.id, "kickoff", "baron's")
    assert linked.client_id == client.id

    cleared = await workspace_service.assign_task_client(user.id, "kickoff", None)
    assert cleared.client_id is None


async def test_get_client_detail_returns_linked_projects_and_tasks(
    db_session: AsyncSession, workspace_service: WorkspaceService
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-ws-9", "owner-ws9@example.com", "Owner")
    await db_session.commit()

    project = await workspace_service.create_project(user.id, "Summer menu", "Baron's")
    await workspace_service.create_task(user.id, "Prep dishes", "summer")
    await workspace_service.create_project(user.id, "Unrelated project")

    detail = await workspace_service.get_client_detail(user.id, "baron's")

    assert detail.client.name == "Baron's"
    assert [s.project.id for s in detail.projects] == [project.id]
    assert [t.title for t in detail.tasks] == ["Prep dishes"]
