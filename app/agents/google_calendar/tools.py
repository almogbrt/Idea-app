from __future__ import annotations

import json
from typing import Any

from app.agents.google_calendar.client import CalendarClient
from app.application.ports.agent_tool import Tool, ToolExecutionContext
from app.domain.entities import ToolResult

AGENT_NAME = "google_calendar"


class ListUpcomingEventsTool(Tool):
    name = "calendar_list_upcoming_events"
    description = "List the user's upcoming Google Calendar events, soonest first."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "max_results": {
                "type": "integer",
                "description": "Maximum number of events to return.",
                "default": 10,
            },
            "time_min": {
                "type": "string",
                "description": "RFC3339 timestamp to start listing from (default: now).",
            },
        },
        "required": [],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: CalendarClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        events = await self._client.list_upcoming_events(
            context.user_id, arguments.get("max_results", 10), arguments.get("time_min")
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(events))


class CreateEventTool(Tool):
    name = "calendar_create_event"
    description = "Create a new event on the user's primary Google Calendar."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "summary": {"type": "string", "description": "Event title."},
            "start_time": {"type": "string", "description": "RFC3339 start datetime."},
            "end_time": {"type": "string", "description": "RFC3339 end datetime."},
            "description": {"type": "string", "description": "Event description (optional)."},
            "attendees": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Attendee email addresses (optional).",
            },
        },
        "required": ["summary", "start_time", "end_time"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: CalendarClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        event = await self._client.create_event(
            context.user_id,
            arguments["summary"],
            arguments["start_time"],
            arguments["end_time"],
            arguments.get("description"),
            arguments.get("attendees"),
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(event))


class DeleteEventTool(Tool):
    name = "calendar_delete_event"
    description = "Delete an event from the user's primary Google Calendar by event ID."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {"event_id": {"type": "string", "description": "Google Calendar event ID."}},
        "required": ["event_id"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: CalendarClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        await self._client.delete_event(context.user_id, arguments["event_id"])
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps({"deleted": True})
        )
