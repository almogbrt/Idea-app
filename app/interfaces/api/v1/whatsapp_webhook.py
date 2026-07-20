"""Meta WhatsApp Business Platform webhook.

There's no logged-in user here — Meta calls this directly — so
authentication is the webhook verification handshake (GET) and an HMAC
signature over the raw body (POST), not the usual `idea_os_session` cookie.

Routing logic: this whole system has exactly one owner. A message from the
owner's own configured number is treated as a command to Edith (routed
through the same Orchestrator the web chat uses, replied to over WhatsApp,
in one durable "WhatsApp" conversation thread). Anything else is a message
with/from a client, just logged — Edith only reads it back when explicitly
asked to (see `app/agents/whatsapp/tools.py`).
"""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, Depends, Header, Query, Request
from fastapi.responses import PlainTextResponse

from app.core.config import Settings, get_settings
from app.core.container import Container, RequestScopedServices
from app.core.exceptions import AuthError
from app.core.logging import get_logger
from app.infrastructure.db.repositories.user_repository import SqlAlchemyUserRepository
from app.infrastructure.whatsapp.client import verify_webhook_signature
from app.interfaces.api.dependencies import get_container

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])
logger = get_logger(__name__)


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str | None = Query(default=None, alias="hub.mode"),
    hub_verify_token: str | None = Query(default=None, alias="hub.verify_token"),
    hub_challenge: str | None = Query(default=None, alias="hub.challenge"),
    settings: Settings = Depends(get_settings),
) -> PlainTextResponse:
    expected = settings.whatsapp_verify_token
    if not expected or hub_mode != "subscribe" or hub_verify_token != expected:
        raise AuthError("Webhook verification failed.")
    return PlainTextResponse(hub_challenge or "")


def _extract_messages(payload: dict[str, Any]) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for message in value.get("messages", []):
                if message.get("type") == "text":
                    messages.append({"from": message["from"], "text": message["text"]["body"]})
    return messages


@router.post("/webhook")
async def receive_webhook(
    request: Request,
    container: Container = Depends(get_container),
    x_hub_signature_256: str | None = Header(default=None, alias="X-Hub-Signature-256"),
) -> dict[str, str]:
    raw_body = await request.body()
    if not verify_webhook_signature(
        container.settings.whatsapp_app_secret, raw_body, x_hub_signature_256
    ):
        raise AuthError("Invalid webhook signature.")

    messages = _extract_messages(await request.json())
    if not messages:
        return {"status": "ignored"}

    async with container.session_factory() as session:
        owners = await SqlAlchemyUserRepository(session).list_all()
        if not owners:
            logger.warning("whatsapp_webhook_no_owner_user")
            return {"status": "no_owner"}
        owner_id = owners[0].id

        scope = container.build_request_scope(session)
        for message in messages:
            await _handle_message(scope, container, owner_id, message["from"], message["text"])
        await session.commit()

    return {"status": "ok"}


async def _handle_message(
    scope: RequestScopedServices,
    container: Container,
    owner_id: uuid.UUID,
    sender: str,
    text: str,
) -> None:
    if sender == container.settings.whatsapp_owner_phone_number:
        conversation = await scope.manage_conversation.get_or_create_by_title(
            owner_id, "WhatsApp"
        )
        result = await scope.orchestrator.handle_command(
            user_id=owner_id, conversation_id=conversation.id, text=text
        )
        await container.whatsapp_client.send_text(sender, result.reply)
    else:
        await scope.manage_whatsapp_messages.log_inbound(owner_id, sender, text)
