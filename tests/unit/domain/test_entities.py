from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.domain.value_objects import OAuthTokenSet


def test_oauth_token_set_is_expired_when_past_expiry() -> None:
    token = OAuthTokenSet(
        access_token="token",
        refresh_token="refresh",
        scopes=("scope-a",),
        expires_at=datetime.now(UTC) - timedelta(minutes=1),
    )
    assert token.is_expired(now=datetime.now(UTC)) is True


def test_oauth_token_set_is_not_expired_before_expiry() -> None:
    token = OAuthTokenSet(
        access_token="token",
        refresh_token="refresh",
        scopes=("scope-a",),
        expires_at=datetime.now(UTC) + timedelta(minutes=5),
    )
    assert token.is_expired(now=datetime.now(UTC)) is False


def test_oauth_token_set_has_scope() -> None:
    token = OAuthTokenSet(
        access_token="token",
        refresh_token=None,
        scopes=("drive.readonly", "gmail.modify"),
        expires_at=datetime.now(UTC),
    )
    assert token.has_scope("drive.readonly") is True
    assert token.has_scope("calendar") is False
