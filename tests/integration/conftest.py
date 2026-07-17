"""Integration test fixtures: a real Postgres (with pgvector) + Redis.

These tests are skipped automatically if `TEST_DATABASE_URL` isn't reachable
(e.g. no Postgres available in the environment). In CI, the workflow spins
up `postgres` (pgvector-enabled) and `redis` services so these run for real.
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models import Base
from app.infrastructure.db.session import create_engine, create_session_factory

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL", "postgresql+asyncpg://idea_os:idea_os@localhost:5432/idea_os_test"
)
TEST_REDIS_URL = os.environ.get("TEST_REDIS_URL", "redis://localhost:6379/1")


def _postgres_available() -> bool:
    import asyncio

    async def _check() -> bool:
        try:
            engine = create_engine(TEST_DATABASE_URL)
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            await engine.dispose()
            return True
        except Exception:
            return False

    return asyncio.run(_check())


requires_postgres = pytest.mark.skipif(
    not _postgres_available(), reason="Postgres (with pgvector) is not reachable"
)


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    engine = create_engine(TEST_DATABASE_URL)
    session_factory = create_session_factory(engine)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session
        await session.rollback()

    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())

    await engine.dispose()
