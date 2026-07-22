from __future__ import annotations

import uuid

from app.application.ports.inbox import InboxPort
from app.domain.entities import EmailSummary


class ManageEmailUseCase:
    def __init__(self, inbox: InboxPort) -> None:
        self._inbox = inbox

    async def list_recent(self, user_id: uuid.UUID, max_results: int = 4) -> list[EmailSummary]:
        return await self._inbox.list_recent(user_id, max_results)
