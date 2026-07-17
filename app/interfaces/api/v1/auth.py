"""Google OAuth2 login: builds the consent URL, handles the callback, issues
our own session JWT as an httpOnly cookie. This system has exactly one
owner, enforced in `AuthenticateUserUseCase`.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Cookie, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.authenticate_user import AuthenticateUserUseCase
from app.core.container import Container
from app.core.exceptions import AuthError
from app.core.logging import get_logger
from app.domain.entities import User
from app.infrastructure.db.repositories.oauth_token_repository import (
    SqlAlchemyOAuthTokenRepository,
)
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.interfaces.api.dependencies import (
    SESSION_COOKIE_NAME,
    get_container,
    get_current_user,
    get_db_session,
)
from app.interfaces.api.schemas.auth import CurrentUserResponse

router = APIRouter(prefix="/auth/google", tags=["auth"])
logger = get_logger(__name__)

_STATE_COOKIE_NAME = "idea_os_oauth_state"


@router.get("/login")
async def login(container: Container = Depends(get_container)) -> RedirectResponse:
    state = str(uuid.uuid4())
    authorization_url = container.google_oauth_client.build_authorization_url(state)
    response = RedirectResponse(url=authorization_url)
    response.set_cookie(
        _STATE_COOKIE_NAME,
        state,
        httponly=True,
        secure=container.settings.is_production,
        samesite="lax",
        max_age=600,
    )
    return response


@router.get("/callback")
async def callback(
    request: Request,
    code: str,
    state: str,
    container: Container = Depends(get_container),
    session: AsyncSession = Depends(get_db_session),
    idea_os_oauth_state: str | None = Cookie(default=None),
) -> RedirectResponse:
    if not idea_os_oauth_state or idea_os_oauth_state != state:
        raise AuthError(
            "OAuth state mismatch — possible CSRF attempt. Please try signing in again."
        )

    tokens, profile = container.google_oauth_client.exchange_code(code, state)

    use_case = AuthenticateUserUseCase(
        user_repository=SqlAlchemyUserRepository(session),
        oauth_token_repository=SqlAlchemyOAuthTokenRepository(session, container.token_cipher),
        allowed_owner_email=container.settings.owner_email or None,
    )
    user = await use_case.execute(profile, tokens)

    access_token = container.session_tokens.issue_access_token(str(user.id))

    response = RedirectResponse(url="/")
    response.delete_cookie(_STATE_COOKIE_NAME)
    response.set_cookie(
        SESSION_COOKIE_NAME,
        access_token,
        httponly=True,
        secure=container.settings.is_production,
        samesite="lax",
        max_age=container.settings.jwt_access_token_ttl_minutes * 60,
    )
    logger.info("user_logged_in", user_id=str(user.id))
    return response


@router.post("/logout")
async def logout() -> JSONResponse:
    response = JSONResponse(content={"status": "logged_out"})
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response


@router.get("/me", response_model=CurrentUserResponse)
async def me(user: User = Depends(get_current_user)) -> CurrentUserResponse:
    return CurrentUserResponse(id=user.id, email=user.email, name=user.name)
