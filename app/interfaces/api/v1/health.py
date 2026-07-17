from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.core.container import Container
from app.core.exceptions import ExternalServiceError
from app.interfaces.api.dependencies import get_container

router = APIRouter(tags=["health"])


@router.get("/health")
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness(container: Container = Depends(get_container)) -> dict[str, str]:
    try:
        async with container.session_factory() as session:
            await session.execute(text("SELECT 1"))
    except Exception as exc:
        raise ExternalServiceError(f"Database is not reachable: {exc}") from exc

    try:
        await container.redis_client.ping()
    except Exception as exc:
        raise ExternalServiceError(f"Redis is not reachable: {exc}") from exc

    return {"status": "ready"}
