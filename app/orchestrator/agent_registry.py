"""Central registry mapping tool name -> `Tool` instance.

This is the extension point of the whole system: `app/agents/__init__.py`
registers every agent's tools into a `Container`'s `AgentRegistry` at
startup. The orchestrator and intent router only ever depend on
`AgentRegistry` — adding a new Agent never requires modifying either of
them. Each `Container` owns its own instance (no shared global state),
so multiple app instances in the same process — as in tests — don't
collide.
"""

from __future__ import annotations

from app.application.ports.agent_tool import Tool
from app.core.exceptions import NotFoundError
from app.core.logging import get_logger
from app.domain.entities import ToolDefinition
from app.orchestrator.base_agent import BaseAgent

logger = get_logger(__name__)


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, BaseAgent] = {}
        self._tools: dict[str, Tool] = {}

    def register(self, agent: BaseAgent) -> None:
        if agent.name in self._agents:
            raise ValueError(f"Agent '{agent.name}' is already registered")

        self._agents[agent.name] = agent
        for tool in agent.get_tools():
            if tool.name in self._tools:
                raise ValueError(f"Tool '{tool.name}' is already registered")
            self._tools[tool.name] = tool

        logger.info(
            "agent_registered",
            agent=agent.name,
            tools=[t.name for t in agent.get_tools()],
        )

    def get_tool(self, name: str) -> Tool:
        tool = self._tools.get(name)
        if tool is None:
            raise NotFoundError(f"Unknown tool '{name}'", details={"tool_name": name})
        return tool

    def all_tool_definitions(self) -> list[ToolDefinition]:
        return [tool.definition() for tool in self._tools.values()]

    def list_agents(self) -> list[str]:
        return list(self._agents.keys())
