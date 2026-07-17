"""Cryptographic primitives: session JWTs and at-rest token encryption.

Two distinct concerns live here:
  * `SessionTokenService` issues/verifies the JWTs our own API uses for
    session auth (set as an httpOnly cookie after Google login succeeds).
  * `TokenCipher` encrypts/decrypts Google OAuth access/refresh tokens
    before they are persisted to Postgres, using a Fernet key sourced from
    Secret Manager (never stored alongside the data it protects).
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

import jwt
from cryptography.fernet import Fernet, InvalidToken

from app.core.exceptions import AuthError


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


@dataclass(frozen=True, slots=True)
class SessionTokenClaims:
    user_id: str
    token_type: TokenType
    expires_at: datetime


class SessionTokenService:
    """Issues and verifies our own session JWTs (HS256)."""

    _ALGORITHM = "HS256"

    def __init__(
        self,
        signing_key: str,
        access_ttl_minutes: int,
        refresh_ttl_days: int,
    ) -> None:
        if not signing_key:
            raise ValueError("JWT signing key must not be empty")
        self._signing_key = signing_key
        self._access_ttl = timedelta(minutes=access_ttl_minutes)
        self._refresh_ttl = timedelta(days=refresh_ttl_days)

    def issue_access_token(self, user_id: str) -> str:
        return self._issue(user_id, TokenType.ACCESS, self._access_ttl)

    def issue_refresh_token(self, user_id: str) -> str:
        return self._issue(user_id, TokenType.REFRESH, self._refresh_ttl)

    def _issue(self, user_id: str, token_type: TokenType, ttl: timedelta) -> str:
        now = datetime.now(UTC)
        payload: dict[str, Any] = {
            "sub": user_id,
            "type": token_type.value,
            "iat": now,
            "exp": now + ttl,
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(payload, self._signing_key, algorithm=self._ALGORITHM)

    def verify(self, token: str, *, expected_type: TokenType) -> SessionTokenClaims:
        try:
            payload = jwt.decode(token, self._signing_key, algorithms=[self._ALGORITHM])
        except jwt.ExpiredSignatureError as exc:
            raise AuthError("Session token has expired") from exc
        except jwt.InvalidTokenError as exc:
            raise AuthError("Invalid session token") from exc

        if payload.get("type") != expected_type.value:
            raise AuthError("Unexpected session token type")

        return SessionTokenClaims(
            user_id=payload["sub"],
            token_type=TokenType(payload["type"]),
            expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
        )


class TokenCipher:
    """Symmetric encryption for OAuth tokens persisted at rest."""

    def __init__(self, encryption_key: str) -> None:
        if not encryption_key:
            raise ValueError("Token encryption key must not be empty")
        self._fernet = Fernet(encryption_key.encode())

    def encrypt(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        try:
            return self._fernet.decrypt(ciphertext.encode()).decode()
        except InvalidToken as exc:
            raise AuthError("Failed to decrypt stored token") from exc
