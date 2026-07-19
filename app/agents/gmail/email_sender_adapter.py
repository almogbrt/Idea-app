from __future__ import annotations

import uuid

from app.agents.gmail.client import GmailClient
from app.application.ports.email_sender import EmailSenderPort


class GmailEmailSenderAdapter(EmailSenderPort):
    def __init__(self, client: GmailClient) -> None:
        self._client = client

    async def send(self, user_id: uuid.UUID, to: str, subject: str, body: str) -> None:
        await self._client.send_message(user_id, to, subject, body)
