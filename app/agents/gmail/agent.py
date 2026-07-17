from __future__ import annotations

from app.agents.gmail.client import GmailClient
from app.agents.gmail.tools import GetEmailTool, ListRecentEmailsTool, SendEmailTool
from app.application.ports.agent_tool import Tool
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory
from app.orchestrator.base_agent import BaseAgent


class GmailAgent(BaseAgent):
    name = "gmail"
    description = "Reads, searches, and sends email through the user's Gmail account."

    def __init__(self, google_clients: GoogleApiClientFactory) -> None:
        self._client = GmailClient(google_clients)

    def get_tools(self) -> list[Tool]:
        return [
            ListRecentEmailsTool(self._client),
            GetEmailTool(self._client),
            SendEmailTool(self._client),
        ]
