"""Integration tests: repositories against a real Postgres + pgvector.

Run with a real database available (see `tests/integration/conftest.py`).
These exercise the actual SQL, not fakes — round-tripping through
SQLAlchemy models, pgvector similarity search, and Fernet-encrypted columns.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from cryptography.fernet import Fernet
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import TokenCipher
from app.domain.entities import (
    AgentExecution,
    ExecutionStatus,
    Message,
    MessageRole,
)
from app.domain.value_objects import OAuthTokenSet
from app.infrastructure.db.repositories.agent_execution_repository import (
    SqlAlchemyAgentExecutionRepository,
)
from app.infrastructure.db.repositories.conversation_repository import (
    SqlAlchemyConversationRepository,
)
from app.infrastructure.db.repositories.memory_repository import SqlAlchemyMemoryRepository
from app.infrastructure.db.repositories.oauth_token_repository import (
    SqlAlchemyOAuthTokenRepository,
)
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
