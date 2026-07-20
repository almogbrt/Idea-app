"""Thin wrapper around the Meta WhatsApp Business Platform (Cloud API).

Unlike the Google agents, there's exactly one WhatsApp Business number for
the whole app (not one per user) — a single access token configured via
`Settings`, not a per-user OAuth token. This client is a `Container`-level
singleton, not built per request.
"""

from __future__ import annotations

import hashlib
import hmac

import httpx

from app.core.exceptions import ExternalServiceError
from app.core.logging import get_logger

logger = get_logger(__name__)

_GRAPH_API_BASE = "https://graph.facebook.com/v20.0"


class WhatsAppClient:
    def __init__(self, access_token: str, phone_number_id: str) -> None:
        self._access_token = access_token
        self._phone_number_id = phone_number_id

    async def send_text(self, to: str, body: str) -> None:
        url = f"{_GRAPH_API_BASE}/{self._phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body},
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers={"Authorization": f"Bearer {self._access_token}"},
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "whatsapp_send_error", status=exc.response.status_code, body=exc.response.text
                )
                raise ExternalServiceError(
                    f"WhatsApp API error sending message: {exc.response.text}"
                ) from exc
            except httpx.HTTPError as exc:
                logger.error("whatsapp_send_error", error=str(exc))
                raise ExternalServiceError(f"WhatsApp API request failed: {exc}") from exc


def verify_webhook_signature(app_secret: str, payload: bytes, signature_header: str | None) -> bool:
    """Verifies Meta's `X-Hub-Signature-256` header (`sha256=<hex digest>`)
    against the raw request body, so we only ever act on payloads that
    actually came from Meta."""
    if not app_secret or not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(app_secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    provided = signature_header.removeprefix("sha256=")
    return hmac.compare_digest(expected, provided)
