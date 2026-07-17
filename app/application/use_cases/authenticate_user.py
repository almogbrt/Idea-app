"""Google login use case.

This system has exactly one owner. If `allowed_owner_email` is configured,
any Google account other than that one is rejected at the door — this is a
personal business OS, not a public multi-tenant product.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.application.ports.oauth_token_repository import OAuthTokenRepositoryPort
from app.application.ports.user_repository import UserRepositoryPort
from app.core.exceptions import ForbiddenError
from app.domain.entities import User
from app.domain.value_objects import OAuthTokenSet


@dataclass(frozen=True, slots=True)
class GoogleProfile:
    sub: str
    email: str
    name: str


class AuthenticateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepositoryPort,
        oauth_token_repository: OAuthTokenRepositoryPort,
        allowed_owner_email: str | None = None,
    ) -> None:
        self._users = user_repository
        self._tokens = oauth_token_repository
        self._allowed_owner_email = (
            allowed_owner_email.lower() if allowed_owner_email else None
        )

    async def execute(self, profile: GoogleProfile, tokens: OAuthTokenSet) -> User:
        if self._allowed_owner_email and profile.email.lower() != self._allowed_owner_email:
            raise ForbiddenError(
                "This IDEA OS instance is restricted to its owner account.",
                details={"attempted_email": profile.email},
            )

        user = await self._users.get_by_google_sub(profile.sub)
        if user is None:
            user = await self._users.create(profile.sub, profile.email, profile.name)

        await self._tokens.save_tokens(user.id, provider="google", tokens=tokens)
        return user
