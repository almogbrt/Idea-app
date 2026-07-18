"""A `MemoryRepositoryPort` that opens its own short-lived session per call.

`SqlAlchemyMemoryRepository` shares the caller's request-scoped `AsyncSession`,
which is torn down as soon as the HTTP response is sent — fine for retrieval
(awaited before the response is built), unsafe for storage if the caller
wants to fire it off in the background without making the user wait on it.
This mirrors the session-per-call pattern already used by
`GoogleApiClientFactory` and `WorkspaceService` for the same reason: it's a
long-lived singleton, not something handed a request's session.
"""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.ports.memory_repository import MemoryRepositoryPort
from app.domain.entities import MemoryRecord
from app.infrastructure.db.repositories.memory_repository import SqlAlchemyMemoryRepository


class BackgroundMemoryRepository(MemoryRepositoryPort):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def store(
        self,
        user_id: uuid.UUID,
        content: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> MemoryRecord:
        async with self._session_factory() as session:
            record = await SqlAlchemyMemoryRepository(session).store(
                user_id, content, embedding, metadata
            )
            await session.commit()
            return record

    async def search(
        self, user_id: uuid.UUID, query_embedding: list[float], top_k: int = 5
    ) -> list[MemoryRecord]:
        async with self._session_factory() as session:
            return await SqlAlchemyMemoryRepository(session).search(
                user_id, query_embedding, top_k=top_k
            )
