"""Central application configuration.

All configuration is read once at process startup via environment variables
(loaded from `.env` in local dev, and from the real process environment /
Secret Manager-injected env vars in Cloud Run). Nothing else in the codebase
should call `os.environ` directly — go through `get_settings()`.
"""

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnv(StrEnum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class SecretManagerBackend(StrEnum):
    ENV = "env"
    GCP = "gcp"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: AppEnv = AppEnv.LOCAL
    app_name: str = "IDEA OS - Edith"
    log_level: str = "INFO"
    api_port: int = 8080

    token_encryption_key: str = Field(default="")
    jwt_signing_key: str = Field(default="")
    jwt_access_token_ttl_minutes: int = 60
    jwt_refresh_token_ttl_days: int = 30

    secret_manager_backend: SecretManagerBackend = SecretManagerBackend.ENV
    gcp_project_id: str = ""

    database_url: str = "postgresql+asyncpg://idea_os:idea_os@localhost:5432/idea_os"
    redis_url: str = "redis://localhost:6379/0"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-5"
    anthropic_max_tokens: int = 4096

    # OpenAI is used only for embeddings (Anthropic has no embeddings endpoint).
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    google_oauth_client_id: str = ""
    google_oauth_client_secret: str = ""
    google_oauth_redirect_uri: str = "http://localhost:8080/api/v1/auth/google/callback"
    google_oauth_scopes: str = "openid email profile"

    owner_email: str = ""

    @field_validator("google_oauth_scopes")
    @classmethod
    def _normalize_scopes(cls, v: str) -> str:
        return " ".join(v.split())

    @property
    def google_oauth_scopes_list(self) -> list[str]:
        return self.google_oauth_scopes.split()

    @property
    def is_production(self) -> bool:
        return self.app_env == AppEnv.PRODUCTION


@lru_cache
def get_settings() -> Settings:
    """Process-wide cached settings singleton."""
    return Settings()
