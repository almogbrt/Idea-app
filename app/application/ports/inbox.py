from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import EmailSummary


class InboxPort(ABC):
    """Narrow read-only view of the user's email inbox, for dashboard stats.

    Deliberately independent of the `gmail` Agent's `Tool` wrapper — the
    dashboard reads this directly, without going through the LLM loop.
    """

    @abstractmethod
    async def count_unread(self, user_id: uuid.UUID) -> int:
        raise NotImplementedError

    @abstractmethod
    async def list_recent(self, user_id: uuid.UUID, max_results: int) -> list[EmailSummary]:
        raise NotImplementedError
