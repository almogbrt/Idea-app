"""Agent auto-registration.

`register_all_agents` registers every built-in agent's tools into the
given `AgentRegistry` (owned by a `Container`). To add a brand-new agent
in the future: create `app/agents/<name>/{agent.py,tools.py,client.py}`,
then add one import + `registry.register(...)` line below — nothing in
the orchestrator, intent router, or API layer needs to change.
"""

from __future__ import annotations

from app.agents.project_management.service import WorkspaceService
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory
from app.orchestrator.agent_registry import AgentRegistry


def register_all_agents(
    google_clients: GoogleApiClientFactory,
    workspace_service: WorkspaceService,
    registry: AgentRegistry,
) -> None:
    from app.agents.gmail.agent import GmailAgent
    from app.agents.google_calendar.agent import GoogleCalendarAgent
    from app.agents.google_drive.agent import GoogleDriveAgent
    from app.agents.google_sheets.agent import GoogleSheetsAgent
    from app.agents.project_management.agent import ProjectManagementAgent

    registry.register(GoogleDriveAgent(google_clients))
    registry.register(GmailAgent(google_clients))
    registry.register(GoogleCalendarAgent(google_clients))
    registry.register(GoogleSheetsAgent(google_clients))
    registry.register(ProjectManagementAgent(workspace_service))
