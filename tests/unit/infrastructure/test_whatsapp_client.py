from __future__ import annotations

import hashlib
import hmac

from app.infrastructure.whatsapp.client import verify_webhook_signature


def _sign(secret: str, payload: bytes) -> str:
    digest = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def test_verify_webhook_signature_accepts_valid_signature() -> None:
    secret = "app-secret"
    payload = b'{"entry": []}'
    signature = _sign(secret, payload)

    assert verify_webhook_signature(secret, payload, signature) is True


def test_verify_webhook_signature_rejects_wrong_secret() -> None:
    payload = b'{"entry": []}'
    signature = _sign("right-secret", payload)

    assert verify_webhook_signature("wrong-secret", payload, signature) is False


def test_verify_webhook_signature_rejects_tampered_payload() -> None:
    secret = "app-secret"
    signature = _sign(secret, b'{"entry": []}')

    assert verify_webhook_signature(secret, b'{"entry": [1]}', signature) is False


def test_verify_webhook_signature_rejects_missing_header() -> None:
    assert verify_webhook_signature("app-secret", b"payload", None) is False


def test_verify_webhook_signature_rejects_malformed_header() -> None:
    assert verify_webhook_signature("app-secret", b"payload", "not-sha256-prefixed") is False


def test_verify_webhook_signature_rejects_empty_secret() -> None:
    signature = _sign("", b"payload")
    assert verify_webhook_signature("", b"payload", signature) is False
