from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import Any

from app.domain.entities import MemoryRecord


class MemoryRepositoryPort(ABC):
    """Long-term memory backed by vector similarity search (pgvector)."""

    @abstractmethod
    async def store(
        self,
        user_id: uuid.UUID,
        content: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> MemoryRecord:
        raise NotImplementedError

    @abstractmethod
    async def search(
        self,
        user_id: uuid.UUID,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[MemoryRecord]:
        """Returns records ordered by descending cosine similarity."""
        raise NotImplementedError
