from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import CashFlowSnapshot


class CashFlowPort(ABC):
    """Read-only view of a few key numbers from the user's own cash-flow
    Google Sheet, for the dashboard finance section — bypasses the LLM
    tool-call loop (same reasoning as `CalendarPort`)."""

    @abstractmethod
    async def get_snapshot(self, user_id: uuid.UUID) -> CashFlowSnapshot | None:
        """`None` means not configured yet, or the expected tab/labels
        weren't found — same "quietly show nothing" treatment either way."""
        raise NotImplementedError
