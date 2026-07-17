from __future__ import annotations

from app.agents.google_sheets.client import SheetsClient
from app.agents.google_sheets.tools import (
    AppendRowTool,
    CreateSpreadsheetTool,
    ReadRangeTool,
    WriteRangeTool,
)
from app.application.ports.agent_tool import Tool
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory
from app.orchestrator.base_agent import BaseAgent


class GoogleSheetsAgent(BaseAgent):
    name = "google_sheets"
    description = "Reads and writes data in the user's Google Sheets spreadsheets."

    def __init__(self, google_clients: GoogleApiClientFactory) -> None:
        self._client = SheetsClient(google_clients)

    def get_tools(self) -> list[Tool]:
        return [
            ReadRangeTool(self._client),
            WriteRangeTool(self._client),
            AppendRowTool(self._client),
            CreateSpreadsheetTool(self._client),
        ]
