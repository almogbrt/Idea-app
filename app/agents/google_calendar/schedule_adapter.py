from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from app.agents.google_calendar.client import CalendarClient
from app.application.ports.schedule import SchedulePort


class CalendarScheduleAdapter(SchedulePort):
    def __init__(self, client: CalendarClient) -> None:
        self._client = client

    async def count_meetings_today(self, user_id: uuid.UUID) -> int:
        now = datetime.now(UTC)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        return await self._client.count_events_between(
            user_id, start_of_day.isoformat(), end_of_day.isoformat()
        )
