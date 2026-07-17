"""Long-term memory read/write, sitting behind embedding generation."""

from __future__ import annotations

import uuid
from typing import Any

from app.application.ports.embedding import EmbeddingPort
from app.application.ports.memory_repository import MemoryRepositoryPort
from app.domain.entities import MemoryRecord


class StoreMemoryUseCase:
    def __init__(
        self, embedding_port: EmbeddingPort, memory_repository: MemoryRepositoryPort
    ) -> None:
        self._embeddings = embedding_port
        self._memory = memory_repository

    async def execute(
        self, user_id: uuid.UUID, content: str, metadata: dict[str, Any] | None = None
    ) -> MemoryRecord:
        embedding = await self._embeddings.embed(content)
        return await self._memory.store(user_id, content, embedding, metadata)


class RetrieveMemoryUseCase:
    def __init__(
        self, embedding_port: EmbeddingPort, memory_repository: MemoryRepositoryPort
    ) -> None:
        self._embeddings = embedding_port
        self._memory = memory_repository

    async def execute(
        self, user_id: uuid.UUID, query: str, top_k: int = 5
    ) -> list[MemoryRecord]:
        query_embedding = await self._embeddings.embed(query)
        return await self._memory.search(user_id, query_embedding, top_k=top_k)
