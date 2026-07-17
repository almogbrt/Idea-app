"""Local-dev secret backend: reads from the process environment (`.env`)."""

from __future__ import annotations

import os

from app.application.ports.secret_manager import SecretManagerPort
from app.core.exceptions import NotFoundError


class EnvSecretManager(SecretManagerPort):
    def get_secret(self, name: str) -> str:
        value = os.environ.get(name)
        if value is None:
            raise NotFoundError(f"Secret '{name}' is not set in the environment")
        return value
