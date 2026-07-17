from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.memory_repository import MemoryRepositoryPort
from app.domain.entities import MemoryRecord
from app.infrastructure.db.models import MemoryRecordModel


class SqlAlchemyMemoryRepository(MemoryRepositoryPort):
    """pgvector-backed long-term memory with cosine-similarity search."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def store(
        self,
        user_id: uuid.UUID,
        content: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> MemoryRecord:
        row = MemoryRecordModel(
            user_id=user_id, content=content, embedding=embedding, record_metadata=metadata or {}
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def search(
        self, user_id: uuid.UUID, query_embedding: list[float], top_k: int = 5
    ) -> list[MemoryRecord]:
        distance = MemoryRecordModel.embedding.cosine_distance(query_embedding)
        stmt = (
            select(MemoryRecordModel, distance.label("distance"))
            .where(MemoryRecordModel.user_id == user_id)
            .order_by(distance)
            .limit(top_k)
        )
        rows = (await self._session.execute(stmt)).all()
        return [self._to_entity(row.MemoryRecordModel, similarity=1 - row.distance) for row in rows]

    @staticmethod
    def _to_entity(row: MemoryRecordModel, similarity: float | None = None) -> MemoryRecord:
        return MemoryRecord(
            id=row.id,
            user_id=row.user_id,
            content=row.content,
            metadata=row.record_metadata,
            created_at=row.created_at,
            embedding=list(row.embedding) if row.embedding is not None else None,
            similarity=similarity,
        )
