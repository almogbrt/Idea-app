from __future__ import annotations

from abc import ABC, abstractmethod


class CachePort(ABC):
    @abstractmethod
    async def get(self, key: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: str, ttl_seconds: int | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError
