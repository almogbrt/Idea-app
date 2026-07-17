"""FastAPI dependency wiring: per-request DB session, container access, current user."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from typing import cast

from fastapi import Cookie, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.container import Container, RequestScopedServices
from app.core.exceptions import AuthError
from app.core.security import TokenType
from app.domain.entities import User
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository

SESSION_COOKIE_NAME = "idea_os_session"


def get_container(request: Request) -> Container:
    return cast(Container, request.app.state.container)


async def get_db_session(
    container: Container = Depends(get_container),
) -> AsyncIterator[AsyncSession]:
    async with container.session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_request_scope(
    session: AsyncSession = Depends(get_db_session),
    container: Container = Depends(get_container),
) -> RequestScopedServices:
    return container.build_request_scope(session)


async def get_current_user(
    session: AsyncSession = Depends(get_db_session),
    container: Container = Depends(get_container),
    idea_os_session: str | None = Cookie(default=None),
) -> User:
    if not idea_os_session:
        raise AuthError("Not authenticated. Please sign in with Google.")

    claims = container.session_tokens.verify(idea_os_session, expected_type=TokenType.ACCESS)
    user = await SqlAlchemyUserRepository(session).get_by_id(uuid.UUID(claims.user_id))
    if user is None:
        raise AuthError("Session refers to a user that no longer exists.")
    return user
