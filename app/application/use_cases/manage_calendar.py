from __future__ import annotations

import uuid

from app.application.ports.calendar_port import CalendarPort
from app.domain.entities import CalendarEvent


class ManageCalendarUseCase:
    def __init__(self, calendar: CalendarPort) -> None:
        self._calendar = calendar

    async def list_between(
        self, user_id: uuid.UUID, time_min: str, time_max: str
    ) -> list[CalendarEvent]:
        return await self._calendar.list_between(user_id, time_min, time_max)

    async def create(
        self,
        user_id: uuid.UUID,
        summary: str,
        start_time: str,
        end_time: str,
        description: str | None = None,
    ) -> CalendarEvent:
        return await self._calendar.create(user_id, summary, start_time, end_time, description)

    async def delete(self, user_id: uuid.UUID, event_id: str) -> None:
        await self._calendar.delete(user_id, event_id)
