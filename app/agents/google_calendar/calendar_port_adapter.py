from __future__ import annotations

import uuid
from typing import Any

from app.agents.google_calendar.client import CalendarClient
from app.application.ports.calendar_port import CalendarPort
from app.domain.entities import CalendarEvent


def _to_entity(raw: dict[str, Any]) -> CalendarEvent:
    start = raw.get("start", {})
    end = raw.get("end", {})
    return CalendarEvent(
        id=raw["id"],
        summary=raw.get("summary", "(ללא כותרת)"),
        start=start.get("dateTime") or start.get("date", ""),
        end=end.get("dateTime") or end.get("date", ""),
        description=raw.get("description"),
        html_link=raw.get("htmlLink"),
    )


class GoogleCalendarPortAdapter(CalendarPort):
    def __init__(self, client: CalendarClient) -> None:
        self._client = client

    async def list_upcoming(self, user_id: uuid.UUID, max_results: int) -> list[CalendarEvent]:
        events = await self._client.list_upcoming_events(user_id, max_results, time_min=None)
        return [_to_entity(e) for e in events]

    async def create(
        self,
        user_id: uuid.UUID,
        summary: str,
        start_time: str,
        end_time: str,
        description: str | None = None,
    ) -> CalendarEvent:
        event = await self._client.create_event(
            user_id, summary, start_time, end_time, description, attendees=None
        )
        return _to_entity(event)

    async def delete(self, user_id: uuid.UUID, event_id: str) -> None:
        await self._client.delete_event(user_id, event_id)
