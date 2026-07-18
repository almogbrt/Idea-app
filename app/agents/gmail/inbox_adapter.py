from __future__ import annotations

import uuid

from app.agents.gmail.client import GmailClient
from app.application.ports.inbox import InboxPort


class GmailInboxAdapter(InboxPort):
    def __init__(self, client: GmailClient) -> None:
        self._client = client

    async def count_unread(self, user_id: uuid.UUID) -> int:
        return await self._client.count_unread(user_id)
