from __future__ import annotations

import uuid
from datetime import UTC

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.oauth_token_repository import OAuthTokenRepositoryPort
from app.core.security import TokenCipher
from app.domain.value_objects import OAuthTokenSet
from app.infrastructure.db.models import OAuthTokenModel


class SqlAlchemyOAuthTokenRepository(OAuthTokenRepositoryPort):
    """Persists OAuth tokens encrypted at rest via `TokenCipher`."""

    def __init__(self, session: AsyncSession, cipher: TokenCipher) -> None:
        self._session = session
        self._cipher = cipher

    async def save_tokens(self, user_id: uuid.UUID, provider: str, tokens: OAuthTokenSet) -> None:
        stmt = (
            insert(OAuthTokenModel)
            .values(
                user_id=user_id,
                provider=provider,
                access_token_enc=self._cipher.encrypt(tokens.access_token),
                refresh_token_enc=(
                    self._cipher.encrypt(tokens.refresh_token) if tokens.refresh_token else None
                ),
                scopes=list(tokens.scopes),
                expiry=tokens.expires_at,
            )
            .on_conflict_do_update(
                index_elements=[OAuthTokenModel.user_id, OAuthTokenModel.provider],
                set_={
                    "access_token_enc": self._cipher.encrypt(tokens.access_token),
                    "refresh_token_enc": (
                        self._cipher.encrypt(tokens.refresh_token)
                        if tokens.refresh_token
                        else None
                    ),
                    "scopes": list(tokens.scopes),
                    "expiry": tokens.expires_at,
                },
            )
        )
        await self._session.execute(stmt)
        await self._session.flush()

    async def get_tokens(self, user_id: uuid.UUID, provider: str) -> OAuthTokenSet | None:
        row = await self._session.scalar(
            select(OAuthTokenModel).where(
                OAuthTokenModel.user_id == user_id, OAuthTokenModel.provider == provider
            )
        )
        if row is None:
            return None

        refresh_token = (
            self._cipher.decrypt(row.refresh_token_enc) if row.refresh_token_enc else None
        )
        expires_at = (
            row.expiry.replace(tzinfo=UTC) if row.expiry.tzinfo is None else row.expiry
        )
        return OAuthTokenSet(
            access_token=self._cipher.decrypt(row.access_token_enc),
            refresh_token=refresh_token,
            scopes=tuple(row.scopes),
            expires_at=expires_at,
        )
