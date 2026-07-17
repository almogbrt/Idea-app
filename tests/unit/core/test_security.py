from __future__ import annotations

import time

import pytest
from cryptography.fernet import Fernet

from app.core.exceptions import AuthError
from app.core.security import SessionTokenService, TokenCipher, TokenType


@pytest.fixture
def token_service() -> SessionTokenService:
    return SessionTokenService(
        signing_key="unit-test-signing-key-that-is-long-enough-32b",
        access_ttl_minutes=60,
        refresh_ttl_days=30,
    )


def test_issue_and_verify_access_token(token_service: SessionTokenService) -> None:
    token = token_service.issue_access_token("user-123")
    claims = token_service.verify(token, expected_type=TokenType.ACCESS)
    assert claims.user_id == "user-123"
    assert claims.token_type == TokenType.ACCESS


def test_verify_rejects_wrong_token_type(token_service: SessionTokenService) -> None:
    token = token_service.issue_refresh_token("user-123")
    with pytest.raises(AuthError):
        token_service.verify(token, expected_type=TokenType.ACCESS)


def test_verify_rejects_expired_token() -> None:
    short_lived = SessionTokenService(
        signing_key="unit-test-signing-key-that-is-long-enough-32b",
        access_ttl_minutes=0,
        refresh_ttl_days=30,
    )
    token = short_lived.issue_access_token("user-123")
    time.sleep(1.2)
    with pytest.raises(AuthError):
        short_lived.verify(token, expected_type=TokenType.ACCESS)


def test_verify_rejects_garbage_token(token_service: SessionTokenService) -> None:
    with pytest.raises(AuthError):
        token_service.verify("not-a-real-token", expected_type=TokenType.ACCESS)


def test_token_cipher_round_trip() -> None:
    cipher = TokenCipher(Fernet.generate_key().decode())
    ciphertext = cipher.encrypt("super-secret-value")
    assert ciphertext != "super-secret-value"
    assert cipher.decrypt(ciphertext) == "super-secret-value"


def test_token_cipher_rejects_wrong_key() -> None:
    cipher_a = TokenCipher(Fernet.generate_key().decode())
    cipher_b = TokenCipher(Fernet.generate_key().decode())
    ciphertext = cipher_a.encrypt("secret")
    with pytest.raises(AuthError):
        cipher_b.decrypt(ciphertext)
