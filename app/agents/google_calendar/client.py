"""Thin wrapper around the Google Calendar v3 API for this agent's needs."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any, cast

from app.agents._shared import call_google_api
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory

_EVENT_FIELDS = "items(id,summary,description,start,end,htmlLink,attendees)"


class CalendarClient:
    def __init__(self, google_clients: GoogleApiClientFactory) -> None:
        self._google_clients = google_clients

    async def list_upcoming_events(
        self, user_id: uuid.UUID, max_results: int, time_min: str | None
    ) -> list[dict[str, Any]]:
        service = await self._google_clients.calendar(user_id)
        effective_time_min = time_min or datetime.now(UTC).isoformat()
        response = await call_google_api(
            lambda: service.events()
            .list(
                calendarId="primary",
                timeMin=effective_time_min,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
                fields=_EVENT_FIELDS,
            )
            .execute(),
            action="calendar.events.list",
        )
        return cast(list[dict[str, Any]], response.get("items", []))

    async def create_event(
        self,
        user_id: uuid.UUID,
        summary: str,
        start_time: str,
        end_time: str,
        description: str | None,
        attendees: list[str] | None,
    ) -> dict[str, Any]:
        service = await self._google_clients.calendar(user_id)
        body: dict[str, Any] = {
            "summary": summary,
            "start": {"dateTime": start_time},
            "end": {"dateTime": end_time},
        }
        if description:
            body["description"] = description
        if attendees:
            body["attendees"] = [{"email": email} for email in attendees]

        return await call_google_api(
            lambda: service.events().insert(calendarId="primary", body=body).execute(),
            action="calendar.events.insert",
        )

    async def delete_event(self, user_id: uuid.UUID, event_id: str) -> None:
        service = await self._google_clients.calendar(user_id)
        await call_google_api(
            lambda: service.events().delete(calendarId="primary", eventId=event_id).execute(),
            action="calendar.events.delete",
        )
