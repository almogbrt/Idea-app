"""Builds authorized Google API client objects for the agents.

Every agent tool needs a live, non-expired `google.oauth2.credentials.Credentials`
for the current user. This factory loads the stored (encrypted) token set,
refreshes it if expired, persists the refreshed token back so the refresh
token rotation doesn't get lost, and hands back a ready-to-use `googleapiclient`
resource (`drive`, `gmail`, `calendar`, `sheets`).

This class is a long-lived singleton shared by every agent (agents are
registered once at process startup), so it must not hold onto a single
request-scoped `AsyncSession`. Instead it opens a short-lived session from
`session_factory` for each token read/write.
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime

from googleapiclient.discovery import Resource, build
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.exceptions import AuthError
from app.core.security import TokenCipher
from app.domain.value_objects import OAuthTokenSet
from app.infrastructure.db.repositories.oauth_token_repository import SqlAlchemyOAuthTokenRepository
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2.credentials import Credentials

_TOKEN_URI = "https://oauth2.googleapis.com/token"  # noqa: S105 - public well-known endpoint


class GoogleApiClientFactory:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        token_cipher: TokenCipher,
        client_id: str,
        client_secret: str,
    ) -> None:
        self._session_factory = session_factory
        self._token_cipher = token_cipher
        self._client_id = client_id
        self._client_secret = client_secret

    async def _get_credentials(self, user_id: uuid.UUID) -> Credentials:
        async with self._session_factory() as session:
            tokens_repo = SqlAlchemyOAuthTokenRepository(session, self._token_cipher)
            token_set = await tokens_repo.get_tokens(user_id, provider="google")
            if token_set is None:
                raise AuthError(
                    "No Google account linked for this user. Please sign in with Google."
                )

            credentials = Credentials(  # type: ignore[no-untyped-call]
                token=token_set.access_token,
                refresh_token=token_set.refresh_token,
                token_uri=_TOKEN_URI,
                client_id=self._client_id,
                client_secret=self._client_secret,
                scopes=list(token_set.scopes),
            )

            if token_set.is_expired(now=datetime.now(UTC)):
                if not token_set.refresh_token:
                    raise AuthError(
                        "Google access token expired and no refresh token is available."
                    )
                await asyncio.to_thread(credentials.refresh, GoogleAuthRequest())
                assert credentials.token is not None  # noqa: S101 - guaranteed by a successful refresh
                await tokens_repo.save_tokens(
                    user_id,
                    provider="google",
                    tokens=OAuthTokenSet(
                        access_token=credentials.token,
                        refresh_token=credentials.refresh_token or token_set.refresh_token,
                        scopes=tuple(credentials.scopes or token_set.scopes),
                        expires_at=(
                            credentials.expiry.replace(tzinfo=UTC)
                            if credentials.expiry and credentials.expiry.tzinfo is None
                            else credentials.expiry or token_set.expires_at
                        ),
                    ),
                )
                await session.commit()

        return credentials

    async def _build(self, service_name: str, version: str, user_id: uuid.UUID) -> Resource:
        credentials = await self._get_credentials(user_id)
        return await asyncio.to_thread(
            build, service_name, version, credentials=credentials, cache_discovery=False
        )

    async def drive(self, user_id: uuid.UUID) -> Resource:
        return await self._build("drive", "v3", user_id)

    async def gmail(self, user_id: uuid.UUID) -> Resource:
        return await self._build("gmail", "v1", user_id)

    async def calendar(self, user_id: uuid.UUID) -> Resource:
        return await self._build("calendar", "v3", user_id)

    async def sheets(self, user_id: uuid.UUID) -> Resource:
        return await self._build("sheets", "v4", user_id)
