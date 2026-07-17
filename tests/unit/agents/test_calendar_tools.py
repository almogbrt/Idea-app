from __future__ import annotations

import json
import uuid
from typing import Any

from app.agents.google_calendar.tools import (
    CreateEventTool,
    DeleteEventTool,
    ListUpcomingEventsTool,
)
from app.application.ports.agent_tool import ToolExecutionContext


class _FakeCalendarClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def list_upcoming_events(
        self, user_id: uuid.UUID, max_results: int, time_min: str | None
    ) -> list[dict]:
        self.calls.append(("list_upcoming_events", (user_id, max_results, time_min)))
        return [{"id": "evt-1", "summary": "Standup"}]

    async def create_event(
        self,
        user_id: uuid.UUID,
        summary: str,
        start_time: str,
        end_time: str,
        description: str | None,
        attendees: list[str] | None,
    ) -> dict:
        self.calls.append(
            ("create_event", (user_id, summary, start_time, end_time, description, attendees))
        )
        return {"id": "evt-new"}

    async def delete_event(self, user_id: uuid.UUID, event_id: str) -> None:
        self.calls.append(("delete_event", (user_id, event_id)))


def _context() -> ToolExecutionContext:
    return ToolExecutionContext(
        user_id=uuid.uuid4(), conversation_id=uuid.uuid4(), correlation_id="corr"
    )


async def test_list_upcoming_events_tool_defaults() -> None:
    client = _FakeCalendarClient()
    tool = ListUpcomingEventsTool(client)
    context = _context()

    result = await tool.execute({}, context)

    assert client.calls == [("list_upcoming_events", (context.user_id, 10, None))]
    assert json.loads(result.content)[0]["summary"] == "Standup"


async def test_create_event_tool_passes_optional_fields() -> None:
    client = _FakeCalendarClient()
    tool = CreateEventTool(client)
    context = _context()

    await tool.execute(
        {
            "summary": "Team sync",
            "start_time": "2026-08-01T10:00:00Z",
            "end_time": "2026-08-01T10:30:00Z",
            "attendees": ["a@example.com"],
        },
        context,
    )

    assert client.calls == [
        (
            "create_event",
            (
                context.user_id,
                "Team sync",
                "2026-08-01T10:00:00Z",
                "2026-08-01T10:30:00Z",
                None,
                ["a@example.com"],
            ),
        )
    ]


async def test_delete_event_tool_reports_success() -> None:
    client = _FakeCalendarClient()
    tool = DeleteEventTool(client)
    context = _context()

    result = await tool.execute({"event_id": "evt-1"}, context)

    assert client.calls == [("delete_event", (context.user_id, "evt-1"))]
    assert json.loads(result.content) == {"deleted": True}
