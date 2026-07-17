from __future__ import annotations

from collections.abc import Iterator

import pytest
from cryptography.fernet import Fernet
from fastapi.testclient import TestClient

from app.core.config import get_settings


@pytest.fixture
def app_env(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    monkeypatch.setenv("TOKEN_ENCRYPTION_KEY", Fernet.generate_key().decode())
    monkeypatch.setenv("JWT_SIGNING_KEY", "test-signing-key-not-for-production")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("GOOGLE_OAUTH_CLIENT_SECRET", "test-client-secret")
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql+asyncpg://idea_os:idea_os@localhost:5432/idea_os_test"
    )
    monkeypatch.setenv("REDIS_URL", "redis://localhost:6379/1")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def client(app_env: None) -> Iterator[TestClient]:
    from app.main import create_app

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
