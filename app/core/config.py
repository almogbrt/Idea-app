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
    jwt_access_token_ttl_minutes: int = 60 * 24 * 30  # 30 days
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

    # The app's own public URL — empty in local dev, filled in at deploy time
    # via the same SERVICE_URL sed substitution as google_oauth_redirect_uri.
    # Used to link back into the app from emails (e.g. the daily review).
    app_base_url: str = ""

    # Shared secret Cloud Scheduler sends as a header when calling the internal
    # reminders endpoint — there's no logged-in user in that context, so this
    # substitutes for a session JWT.
    scheduler_shared_secret: str = ""

    # WhatsApp Business Platform (Meta Cloud API). Empty by default — the
    # webhook/agent simply don't do anything until these are configured.
    whatsapp_access_token: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_app_secret: str = ""
    whatsapp_verify_token: str = ""
    whatsapp_owner_phone_number: str = ""
    """The owner's own personal number (E.164, e.g. 9725xxxxxxxx) — inbound
    messages from this number are routed to Edith as chat commands instead
    of being logged as a client conversation."""

    # Green Invoice (חשבונית ירוקה) — read-only income/expense dashboard
    # integration. Empty by default; the finance section simply shows no
    # data until these are configured.
    green_invoice_api_id: str = ""
    green_invoice_api_secret: str = ""
    green_invoice_base_url: str = "https://api.greeninvoice.co.il/api/v1"

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
