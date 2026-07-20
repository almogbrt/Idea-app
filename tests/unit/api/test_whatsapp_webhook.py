from __future__ import annotations

import uuid
from dataclasses import dataclass

import pytest
from fastapi.testclient import TestClient

from app.application.use_cases.manage_conversation import ManageConversationUseCase
from app.application.use_cases.manage_whatsapp_messages import ManageWhatsAppMessagesUseCase
from app.domain.entities import OrchestrationResult
from app.interfaces.api.v1.whatsapp_webhook import _extract_messages, _handle_message
from tests.conftest import FakeConversationRepository, FakeWhatsAppMessageRepository


def test_extract_messages_returns_only_text_messages() -> None:
    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {"from": "972500000000", "type": "text", "text": {"body": "hi"}},
                                {"from": "972500000001", "type": "image"},
                            ]
                        }
                    }
                ]
            }
        ]
    }

    messages = _extract_messages(payload)

    assert messages == [{"from": "972500000000", "text": "hi"}]


def test_extract_messages_handles_no_messages_key() -> None:
    assert _extract_messages({"entry": [{"changes": [{"value": {}}]}]}) == []


def test_extract_messages_handles_empty_payload() -> None:
    assert _extract_messages({}) == []


class _FakeOrchestrator:
    def __init__(self, reply: str) -> None:
        self.reply = reply
        self.calls: list[dict[str, object]] = []

    async def handle_command(
        self, *, user_id: uuid.UUID, conversation_id: uuid.UUID, text: str
    ) -> OrchestrationResult:
        self.calls.append({"user_id": user_id, "conversation_id": conversation_id, "text": text})
        return OrchestrationResult(reply=self.reply, conversation_id=conversation_id)


class _FakeWhatsAppClient:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    async def send_text(self, to: str, body: str) -> None:
        self.sent.append((to, body))


@dataclass
class _FakeSettings:
    whatsapp_owner_phone_number: str


@dataclass
class _FakeContainer:
    settings: _FakeSettings
    whatsapp_client: _FakeWhatsAppClient


@dataclass
class _FakeScope:
    manage_conversation: ManageConversationUseCase
    orchestrator: _FakeOrchestrator
    manage_whatsapp_messages: ManageWhatsAppMessagesUseCase


async def test_handle_message_from_owner_routes_to_orchestrator_and_replies() -> None:
    user_id = uuid.uuid4()
    orchestrator = _FakeOrchestrator(reply="Sure, done.")
    whatsapp_client = _FakeWhatsAppClient()
    container = _FakeContainer(
        settings=_FakeSettings(whatsapp_owner_phone_number="972500000000"),
        whatsapp_client=whatsapp_client,
    )
    scope = _FakeScope(
        manage_conversation=ManageConversationUseCase(FakeConversationRepository()),
        orchestrator=orchestrator,
        manage_whatsapp_messages=ManageWhatsAppMessagesUseCase(FakeWhatsAppMessageRepository()),
    )

    await _handle_message(scope, container, user_id, "972500000000", "create a task")  # type: ignore[arg-type]

    assert len(orchestrator.calls) == 1
    assert orchestrator.calls[0]["text"] == "create a task"
    assert whatsapp_client.sent == [("972500000000", "Sure, done.")]


async def test_handle_message_from_owner_reuses_same_conversation() -> None:
    user_id = uuid.uuid4()
    container = _FakeContainer(
        settings=_FakeSettings(whatsapp_owner_phone_number="972500000000"),
        whatsapp_client=_FakeWhatsAppClient(),
    )
    scope = _FakeScope(
        manage_conversation=ManageConversationUseCase(FakeConversationRepository()),
        orchestrator=_FakeOrchestrator(reply="ok"),
        manage_whatsapp_messages=ManageWhatsAppMessagesUseCase(FakeWhatsAppMessageRepository()),
    )

    await _handle_message(scope, container, user_id, "972500000000", "first")  # type: ignore[arg-type]
    await _handle_message(scope, container, user_id, "972500000000", "second")  # type: ignore[arg-type]

    conversation_ids = {call["conversation_id"] for call in scope.orchestrator.calls}
    assert len(conversation_ids) == 1


async def test_handle_message_from_client_is_logged_not_routed_to_orchestrator() -> None:
    user_id = uuid.uuid4()
    messages_repo = FakeWhatsAppMessageRepository()
    orchestrator = _FakeOrchestrator(reply="should not be called")
    container = _FakeContainer(
        settings=_FakeSettings(whatsapp_owner_phone_number="972500000000"),
        whatsapp_client=_FakeWhatsAppClient(),
    )
    scope = _FakeScope(
        manage_conversation=ManageConversationUseCase(FakeConversationRepository()),
        orchestrator=orchestrator,
        manage_whatsapp_messages=ManageWhatsAppMessagesUseCase(messages_repo),
    )

    await _handle_message(
        scope, container, user_id, "972511111111", "hey, are we still on for Tuesday?"
    )  # type: ignore[arg-type]

    assert orchestrator.calls == []
    assert len(messages_repo.messages) == 1
    assert messages_repo.messages[0].phone_number == "972511111111"
    assert messages_repo.messages[0].content == "hey, are we still on for Tuesday?"


def test_webhook_verification_handshake_returns_challenge(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.core import config as config_module

    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "my-verify-token")
    config_module.get_settings.cache_clear()
    try:
        response = client.get(
            "/api/v1/whatsapp/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "my-verify-token",
                "hub.challenge": "12345",
            },
        )
        assert response.status_code == 200
        assert response.text == "12345"
    finally:
        config_module.get_settings.cache_clear()


def test_webhook_verification_handshake_rejects_wrong_token(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.core import config as config_module

    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "my-verify-token")
    config_module.get_settings.cache_clear()
    try:
        response = client.get(
            "/api/v1/whatsapp/webhook",
            params={
                "hub.mode": "subscribe",
                "hub.verify_token": "wrong-token",
                "hub.challenge": "12345",
            },
        )
        assert response.status_code == 401
    finally:
        config_module.get_settings.cache_clear()
