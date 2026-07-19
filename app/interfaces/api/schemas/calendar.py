from __future__ import annotations

from pydantic import BaseModel, Field


class CalendarEventView(BaseModel):
    id: str
    summary: str
    start: str
    end: str
    description: str | None = None
    html_link: str | None = None


class CreateCalendarEventRequest(BaseModel):
    summary: str = Field(..., min_length=1, max_length=500)
    start_time: str
    end_time: str
    description: str | None = None
