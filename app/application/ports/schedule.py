from __future__ import annotations

import uuid
from abc import ABC, abstractmethod


class SchedulePort(ABC):
    """Narrow read-only view of the user's calendar, for dashboard stats."""

    @abstractmethod
    async def count_meetings_today(self, user_id: uuid.UUID) -> int:
        raise NotImplementedError
