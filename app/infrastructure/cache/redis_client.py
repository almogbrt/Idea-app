from __future__ import annotations

from redis.asyncio import Redis, from_url

from app.application.ports.cache import CachePort


def create_redis_client(redis_url: str) -> Redis:
    return from_url(redis_url, decode_responses=True)


class RedisCache(CachePort):
    def __init__(self, client: Redis) -> None:
        self._client = client

    async def get(self, key: str) -> str | None:
        value = await self._client.get(key)
        return str(value) if value is not None else None

    async def set(self, key: str, value: str, ttl_seconds: int | None = None) -> None:
        await self._client.set(key, value, ex=ttl_seconds)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)
