"""Production secret backend: Google Cloud Secret Manager.

Fetches the `latest` version of a secret named `{name}` in the configured
GCP project. Secret Manager access itself is authorized via the Cloud Run
service's attached service account — no credentials live in this code.
"""

from __future__ import annotations

from functools import lru_cache

from google.api_core.exceptions import GoogleAPIError, NotFound
from google.cloud import secretmanager

from app.application.ports.secret_manager import SecretManagerPort
from app.core.exceptions import ExternalServiceError, NotFoundError
from app.core.logging import get_logger

logger = get_logger(__name__)


class GcpSecretManager(SecretManagerPort):
    def __init__(self, project_id: str) -> None:
        self._project_id = project_id
        self._client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, name: str) -> str:
        return self._get_secret_cached(name)

    @lru_cache(maxsize=64)  # noqa: B019 - bounded, process-lifetime secret cache is intentional
    def _get_secret_cached(self, name: str) -> str:
        secret_path = f"projects/{self._project_id}/secrets/{name}/versions/latest"
        try:
            response = self._client.access_secret_version(name=secret_path)
        except NotFound as exc:
            raise NotFoundError(f"Secret '{name}' not found in Secret Manager") from exc
        except GoogleAPIError as exc:
            logger.error("secret_manager_error", secret=name, error=str(exc))
            raise ExternalServiceError(f"Secret Manager error fetching '{name}': {exc}") from exc

        return response.payload.data.decode("utf-8")
