from __future__ import annotations

from app.agents.project_management.service import WorkspaceService
from app.agents.project_management.tools import (
    CreateClientTool,
    CreateProjectTool,
    CreateTaskTool,
    GetClientDetailTool,
    ListProjectsTool,
    ListTasksTool,
    UpdateClientTool,
    UpdateProjectStatusTool,
    UpdateTaskStatusTool,
)
from app.application.ports.agent_tool import Tool
from app.orchestrator.base_agent import BaseAgent


class ProjectManagementAgent(BaseAgent):
    name = "project_management"
    description = "Manages the user's clients, projects, and tasks."

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    def get_tools(self) -> list[Tool]:
        return [
            CreateClientTool(self._service),
            UpdateClientTool(self._service),
            GetClientDetailTool(self._service),
            CreateProjectTool(self._service),
            UpdateProjectStatusTool(self._service),
            ListProjectsTool(self._service),
            CreateTaskTool(self._service),
            UpdateTaskStatusTool(self._service),
            ListTasksTool(self._service),
        ]
