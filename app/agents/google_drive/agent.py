from __future__ import annotations

from app.agents.google_drive.client import DriveClient
from app.agents.google_drive.tools import (
    CreateFileTool,
    GetFileContentTool,
    ListFilesTool,
    ShareFileTool,
)
from app.application.ports.agent_tool import Tool
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory
from app.orchestrator.base_agent import BaseAgent


class GoogleDriveAgent(BaseAgent):
    name = "google_drive"
    description = "Reads, creates, and shares files in the user's Google Drive."

    def __init__(self, google_clients: GoogleApiClientFactory) -> None:
        self._client = DriveClient(google_clients)

    def get_tools(self) -> list[Tool]:
        return [
            ListFilesTool(self._client),
            GetFileContentTool(self._client),
            CreateFileTool(self._client),
            ShareFileTool(self._client),
        ]
