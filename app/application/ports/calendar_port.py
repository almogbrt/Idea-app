from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import CalendarEvent


class CalendarPort(ABC):
    """Read/write view of the user's Google Calendar, for the dashboard
    calendar section — goes straight to the Calendar API, bypassing the LLM
    tool-call loop (same reasoning as `InboxPort`/`SchedulePort`)."""

    @abstractmethod
    async def list_between(
        self, user_id: uuid.UUID, time_min: str, time_max: str
    ) -> list[CalendarEvent]:
        """Events starting within [time_min, time_max) — both ISO 8601. Used
        both for the dashboard's "today" card and the full month view, just
        with a different range."""
        raise NotImplementedError

    @abstractmethod
    async def create(
        self,
        user_id: uuid.UUID,
        summary: str,
        start_time: str,
        end_time: str,
        description: str | None = None,
    ) -> CalendarEvent:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: uuid.UUID, event_id: str) -> None:
        raise NotImplementedError
