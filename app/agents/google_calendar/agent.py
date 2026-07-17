from __future__ import annotations

from app.agents.google_calendar.client import CalendarClient
from app.agents.google_calendar.tools import (
    CreateEventTool,
    DeleteEventTool,
    ListUpcomingEventsTool,
)
from app.application.ports.agent_tool import Tool
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory
from app.orchestrator.base_agent import BaseAgent


class GoogleCalendarAgent(BaseAgent):
    name = "google_calendar"
    description = "Reads, creates, and deletes events on the user's Google Calendar."

    def __init__(self, google_clients: GoogleApiClientFactory) -> None:
        self._client = CalendarClient(google_clients)

    def get_tools(self) -> list[Tool]:
        return [
            ListUpcomingEventsTool(self._client),
            CreateEventTool(self._client),
            DeleteEventTool(self._client),
        ]
