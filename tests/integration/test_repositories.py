"""Integration tests: repositories against a real Postgres + pgvector.

Run with a real database available (see `tests/integration/conftest.py`).
These exercise the actual SQL, not fakes — round-tripping through
SQLAlchemy models, pgvector similarity search, and Fernet-encrypted columns.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest
from cryptography.fernet import Fernet
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.core.security import TokenCipher
from app.domain.entities import (
    AgentExecution,
    ExecutionStatus,
    Message,
    MessageRole,
    ProjectType,
    TaskStatus,
)
from app.domain.value_objects import OAuthTokenSet
from app.infrastructure.db.repositories.agent_execution_repository import (
    SqlAlchemyAgentExecutionRepository,
)
from app.infrastructure.db.repositories.client_repository import SqlAlchemyClientRepository
from app.infrastructure.db.repositories.conversation_repository import (
    SqlAlchemyConversationRepository,
)
from app.infrastructure.db.repositories.memory_repository import SqlAlchemyMemoryRepository
from app.infrastructure.db.repositories.oauth_token_repository import (
    SqlAlchemyOAuthTokenRepository,
)
from app.infrastructure.db.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.db.repositories.task_repository import SqlAlchemyTaskRepository
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from tests.integration.conftest import requires_postgres

pytestmark = requires_postgres

EMBEDDING_DIM = 1536


def _one_hot(index: int) -> list[float]:
    vector = [0.0] * EMBEDDING_DIM
    vector[index] = 1.0
    return vector


async def test_user_repository_create_and_lookup(db_session: AsyncSession) -> None:
    repo = SqlAlchemyUserRepository(db_session)

    created = await repo.create("google-sub-1", "owner@example.com", "Owner")
    by_sub = await repo.get_by_google_sub("google-sub-1")
    by_id = await repo.get_by_id(created.id)

    assert by_sub is not None and by_sub.id == created.id
    assert by_id is not None and by_id.email == "owner@example.com"
    assert await repo.get_by_google_sub("nonexistent") is None


async def test_conversation_repository_round_trip(db_session: AsyncSession) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-2", "owner2@example.com", "Owner Two")

    conversations = SqlAlchemyConversationRepository(db_session)
    conversation = await conversations.create_conversation(user.id, "My chat")

    for i in range(3):
        await conversations.append_message(
            Message(
                id=uuid.uuid4(),
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content=f"message {i}",
                created_at=datetime.now(UTC),
            )
        )

    fetched = await conversations.get_conversation(conversation.id)
    history = await conversations.get_recent_messages(conversation.id, limit=2)

    assert fetched is not None and fetched.title == "My chat"
    assert [m.content for m in history] == ["message 1", "message 2"]


async def test_memory_repository_cosine_similarity_search(db_session: AsyncSession) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-3", "owner3@example.com", "Owner Three")

    memory = SqlAlchemyMemoryRepository(db_session)
    await memory.store(user.id, "fact about mornings", _one_hot(0))
    await memory.store(user.id, "fact about evenings", _one_hot(1))
    await memory.store(user.id, "unrelated fact", _one_hot(2))

    results = await memory.search(user.id, _one_hot(0), top_k=2)

    assert len(results) == 2
    assert results[0].content == "fact about mornings"
    assert results[0].similarity is not None and results[0].similarity > 0.99


async def test_memory_repository_scopes_search_by_user(db_session: AsyncSession) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user_a = await users.create("google-sub-4", "a@example.com", "A")
    user_b = await users.create("google-sub-5", "b@example.com", "B")

    memory = SqlAlchemyMemoryRepository(db_session)
    await memory.store(user_a.id, "A's fact", _one_hot(0))
    await memory.store(user_b.id, "B's fact", _one_hot(0))

    results = await memory.search(user_a.id, _one_hot(0), top_k=5)

    assert len(results) == 1
    assert results[0].content == "A's fact"


async def test_oauth_token_repository_encrypts_at_rest(db_session: AsyncSession) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-6", "owner6@example.com", "Owner Six")

    cipher = TokenCipher(Fernet.generate_key().decode())
    repo = SqlAlchemyOAuthTokenRepository(db_session, cipher)
    tokens = OAuthTokenSet(
        access_token="plaintext-access-token",
        refresh_token="plaintext-refresh-token",
        scopes=("drive.readonly",),
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )

    await repo.save_tokens(user.id, "google", tokens)
    await db_session.flush()

    raw_row = (
        await db_session.execute(
            text(
                "SELECT access_token_enc, refresh_token_enc FROM oauth_tokens WHERE user_id = :uid"
            ),
            {"uid": str(user.id)},
        )
    ).one()
    assert "plaintext-access-token" not in raw_row[0]
    assert "plaintext-refresh-token" not in raw_row[1]

    retrieved = await repo.get_tokens(user.id, "google")
    assert retrieved is not None
    assert retrieved.access_token == "plaintext-access-token"
    assert retrieved.refresh_token == "plaintext-refresh-token"


async def test_oauth_token_repository_upsert_overwrites(db_session: AsyncSession) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-7", "owner7@example.com", "Owner Seven")

    cipher = TokenCipher(Fernet.generate_key().decode())
    repo = SqlAlchemyOAuthTokenRepository(db_session, cipher)
    first = OAuthTokenSet(
        access_token="first-token",
        refresh_token="refresh",
        scopes=("a",),
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )
    second = OAuthTokenSet(
        access_token="second-token",
        refresh_token="refresh",
        scopes=("a", "b"),
        expires_at=datetime.now(UTC) + timedelta(hours=2),
    )

    await repo.save_tokens(user.id, "google", first)
    await repo.save_tokens(user.id, "google", second)

    retrieved = await repo.get_tokens(user.id, "google")
    assert retrieved is not None
    assert retrieved.access_token == "second-token"
    assert retrieved.scopes == ("a", "b")


async def test_agent_execution_repository_records_audit_trail(db_session: AsyncSession) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-8", "owner8@example.com", "Owner Eight")

    repo = SqlAlchemyAgentExecutionRepository(db_session)
    await repo.record(
        AgentExecution(
            id=uuid.uuid4(),
            user_id=user.id,
            agent_name="google_drive",
            tool_name="drive_list_files",
            input={"query": "invoice"},
            output={"content": "[]", "is_error": False},
            status=ExecutionStatus.SUCCESS,
            latency_ms=42,
            created_at=datetime.now(UTC),
        )
    )
    await db_session.flush()

    row = (
        await db_session.execute(
            text(
                "SELECT tool_name, status FROM agent_executions WHERE user_id = :uid"
            ),
            {"uid": str(user.id)},
        )
    ).one()
    assert row[0] == "drive_list_files"
    assert row[1] == "success"


async def test_agent_execution_repository_list_recent_orders_newest_first(
    db_session: AsyncSession,
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-9", "owner9@example.com", "Owner Nine")

    repo = SqlAlchemyAgentExecutionRepository(db_session)
    for tool_name in ["tool_a", "tool_b", "tool_c"]:
        await repo.record(
            AgentExecution(
                id=uuid.uuid4(),
                user_id=user.id,
                agent_name="gmail",
                tool_name=tool_name,
                input={},
                output={},
                status=ExecutionStatus.SUCCESS,
                latency_ms=1,
                created_at=datetime.now(UTC),
            )
        )

    recent = await repo.list_recent(user.id, limit=2)

    assert len(recent) == 2
    assert recent[0].tool_name == "tool_c"
    assert recent[1].tool_name == "tool_b"


async def test_client_repository_create_and_list(db_session: AsyncSession) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-10", "owner10@example.com", "Owner Ten")

    repo = SqlAlchemyClientRepository(db_session)
    await repo.create(user.id, "Baron's")

    clients = await repo.list_by_user(user.id)
    assert [c.name for c in clients] == ["Baron's"]


async def test_client_repository_get_and_update(db_session: AsyncSession) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-10b", "owner10b@example.com", "Owner Ten B")

    repo = SqlAlchemyClientRepository(db_session)
    client = await repo.create(user.id, "Baron's")

    fetched = await repo.get(client.id)
    assert fetched is not None
    assert fetched.email is None

    updated = await repo.update(client.id, email="baron@example.com", phone="050-1234567")
    assert updated.email == "baron@example.com"
    assert updated.phone == "050-1234567"
    assert updated.name == "Baron's"

    refetched = await repo.get(client.id)
    assert refetched is not None
    assert refetched.email == "baron@example.com"

    logo_updated = await repo.update(client.id, logo_file_id="drive-file-123")
    assert logo_updated.logo_file_id == "drive-file-123"


async def test_client_repository_update_missing_client_raises(db_session: AsyncSession) -> None:
    repo = SqlAlchemyClientRepository(db_session)
    with pytest.raises(NotFoundError):
        await repo.update(uuid.uuid4(), email="x@example.com")


async def test_project_repository_round_trip_with_client_and_task(
    db_session: AsyncSession,
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-11", "owner11@example.com", "Owner Eleven")

    clients_repo = SqlAlchemyClientRepository(db_session)
    client = await clients_repo.create(user.id, "Baron's")

    projects_repo = SqlAlchemyProjectRepository(db_session)
    project = await projects_repo.create(
        user.id, "Summer menu", client_id=client.id, type=ProjectType.CONSULTING
    )

    tasks_repo = SqlAlchemyTaskRepository(db_session)
    await tasks_repo.create(user.id, "Prep summer menu", project_id=project.id)

    summaries = await projects_repo.list_by_user(user.id)
    assert len(summaries) == 1
    assert summaries[0].client_name == "Baron's"
    assert summaries[0].last_task_title == "Prep summer menu"

    single_summary = await projects_repo.get_summary(project.id)
    assert single_summary is not None
    assert single_summary.client_name == "Baron's"

    updated = await projects_repo.update_type(project.id, ProjectType.MENTORING)
    assert updated.type == ProjectType.MENTORING

    active_count = await projects_repo.count_active(user.id)
    assert active_count == 1

    other_client = await clients_repo.create(user.id, "Other Co")
    reassigned = await projects_repo.assign_client(project.id, other_client.id)
    assert reassigned.client_id == other_client.id


async def test_project_repository_delete_unlinks_tasks_instead_of_deleting_them(
    db_session: AsyncSession,
) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-13", "owner13@example.com", "Owner Thirteen")

    clients_repo = SqlAlchemyClientRepository(db_session)
    client = await clients_repo.create(user.id, "Baron's")

    projects_repo = SqlAlchemyProjectRepository(db_session)
    project = await projects_repo.create(
        user.id, "Summer menu", client_id=client.id, type=ProjectType.CONSULTING
    )

    tasks_repo = SqlAlchemyTaskRepository(db_session)
    task = await tasks_repo.create(user.id, "Prep summer menu", project_id=project.id)

    await projects_repo.delete(project.id)

    assert await projects_repo.get(project.id) is None
    surviving_task = await tasks_repo.get(task.id)
    assert surviving_task is not None
    assert surviving_task.project_id is None


async def test_project_repository_delete_missing_project_raises(
    db_session: AsyncSession,
) -> None:
    projects_repo = SqlAlchemyProjectRepository(db_session)
    with pytest.raises(NotFoundError):
        await projects_repo.delete(uuid.uuid4())


async def test_task_repository_round_trip_and_count_open(db_session: AsyncSession) -> None:
    users = SqlAlchemyUserRepository(db_session)
    user = await users.create("google-sub-12", "owner12@example.com", "Owner Twelve")

    tasks_repo = SqlAlchemyTaskRepository(db_session)
    task_a = await tasks_repo.create(user.id, "Task A")
    await tasks_repo.create(user.id, "Task B")

    assert await tasks_repo.count_open(user.id) == 2

    await tasks_repo.update_status(task_a.id, TaskStatus.DONE)

    assert await tasks_repo.count_open(user.id) == 1
    tasks = await tasks_repo.list_by_user(user.id)
    assert {t.title for t in tasks} == {"Task A", "Task B"}
