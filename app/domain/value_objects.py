"""Pure value objects — immutable, no framework or infrastructure dependency."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class OAuthTokenSet:
    """A decrypted OAuth token pair, as used in-memory once loaded from storage."""

    access_token: str
    refresh_token: str | None
    scopes: tuple[str, ...]
    expires_at: datetime

    def is_expired(self, *, now: datetime) -> bool:
        return now >= self.expires_at

    def has_scope(self, scope: str) -> bool:
        return scope in self.scopes
