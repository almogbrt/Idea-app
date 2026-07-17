from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from app.application.use_cases.authenticate_user import AuthenticateUserUseCase, GoogleProfile
from app.core.exceptions import ForbiddenError
from app.domain.value_objects import OAuthTokenSet
from tests.conftest import FakeOAuthTokenRepository, FakeUserRepository

_TOKENS = OAuthTokenSet(
    access_token="access",
    refresh_token="refresh",
    scopes=("openid", "email"),
    expires_at=datetime.now(UTC) + timedelta(hours=1),
)


async def test_creates_new_user_on_first_login(
    fake_user_repository: FakeUserRepository, fake_oauth_token_repository: FakeOAuthTokenRepository
) -> None:
    use_case = AuthenticateUserUseCase(fake_user_repository, fake_oauth_token_repository)
    profile = GoogleProfile(sub="google-sub-1", email="owner@example.com", name="Owner")

    user = await use_case.execute(profile, _TOKENS)

    assert user.google_sub == "google-sub-1"
    assert user.email == "owner@example.com"
    stored_tokens = await fake_oauth_token_repository.get_tokens(user.id, "google")
    assert stored_tokens == _TOKENS


async def test_reuses_existing_user_on_subsequent_login(
    fake_user_repository: FakeUserRepository, fake_oauth_token_repository: FakeOAuthTokenRepository
) -> None:
    use_case = AuthenticateUserUseCase(fake_user_repository, fake_oauth_token_repository)
    profile = GoogleProfile(sub="google-sub-1", email="owner@example.com", name="Owner")

    first = await use_case.execute(profile, _TOKENS)
    second = await use_case.execute(profile, _TOKENS)

    assert first.id == second.id
    assert len(fake_user_repository.users) == 1


async def test_rejects_non_owner_email_when_restricted(
    fake_user_repository: FakeUserRepository, fake_oauth_token_repository: FakeOAuthTokenRepository
) -> None:
    use_case = AuthenticateUserUseCase(
        fake_user_repository, fake_oauth_token_repository, allowed_owner_email="owner@example.com"
    )
    profile = GoogleProfile(sub="intruder-sub", email="intruder@example.com", name="Intruder")

    with pytest.raises(ForbiddenError):
        await use_case.execute(profile, _TOKENS)

    assert len(fake_user_repository.users) == 0


async def test_allows_owner_email_case_insensitively(
    fake_user_repository: FakeUserRepository, fake_oauth_token_repository: FakeOAuthTokenRepository
) -> None:
    use_case = AuthenticateUserUseCase(
        fake_user_repository, fake_oauth_token_repository, allowed_owner_email="Owner@Example.com"
    )
    profile = GoogleProfile(sub="google-sub-1", email="owner@example.com", name="Owner")

    user = await use_case.execute(profile, _TOKENS)
    assert user.email == "owner@example.com"
