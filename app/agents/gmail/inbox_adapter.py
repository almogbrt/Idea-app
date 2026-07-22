from __future__ import annotations

import uuid

from app.agents.gmail.client import GmailClient
from app.application.ports.inbox import InboxPort
from app.domain.entities import EmailSummary


class GmailInboxAdapter(InboxPort):
    def __init__(self, client: GmailClient) -> None:
        self._client = client

    async def count_unread(self, user_id: uuid.UUID) -> int:
        return await self._client.count_unread(user_id)

    async def list_recent(self, user_id: uuid.UUID, max_results: int) -> list[EmailSummary]:
        messages = await self._client.list_messages(user_id, query=None, max_results=max_results)
        return [
            EmailSummary(
                id=m["id"],
                sender=m["from"],
                subject=m["subject"],
                snippet=m["snippet"],
                date=m["date"],
            )
            for m in messages
        ]
