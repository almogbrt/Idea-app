from __future__ import annotations

from typing import Any

import pytest

from app.application.ports.agent_tool import Tool, ToolExecutionContext
from app.core.exceptions import NotFoundError
from app.domain.entities import ToolResult
from app.orchestrator.agent_registry import AgentRegistry
from app.orchestrator.base_agent import BaseAgent


class _EchoTool(Tool):
    def __init__(self, name: str, agent_name: str) -> None:
        self.name = name
        self.description = f"Echo tool for {name}"
        self.parameters_schema: dict[str, Any] = {"type": "object", "properties": {}}
        self.agent_name = agent_name

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        return ToolResult(tool_call_id="", tool_name=self.name, content="echo")


class _FakeAgent(BaseAgent):
    def __init__(self, name: str, tool_names: list[str]) -> None:
        self.name = name
        self.description = f"Fake agent {name}"
        self._tools = [_EchoTool(tool_name, name) for tool_name in tool_names]

    def get_tools(self) -> list[Tool]:
        return self._tools


def test_register_exposes_all_tool_definitions() -> None:
    registry = AgentRegistry()
    registry.register(_FakeAgent("agent_a", ["tool_1", "tool_2"]))

    definitions = registry.all_tool_definitions()

    assert {d.name for d in definitions} == {"tool_1", "tool_2"}
    assert registry.list_agents() == ["agent_a"]


def test_register_rejects_duplicate_agent_name() -> None:
    registry = AgentRegistry()
    registry.register(_FakeAgent("agent_a", ["tool_1"]))
    with pytest.raises(ValueError):
        registry.register(_FakeAgent("agent_a", ["tool_2"]))


def test_register_rejects_duplicate_tool_name_across_agents() -> None:
    registry = AgentRegistry()
    registry.register(_FakeAgent("agent_a", ["shared_tool"]))
    with pytest.raises(ValueError):
        registry.register(_FakeAgent("agent_b", ["shared_tool"]))


def test_get_tool_raises_not_found_for_unknown_tool() -> None:
    registry = AgentRegistry()
    with pytest.raises(NotFoundError):
        registry.get_tool("does_not_exist")


def test_get_tool_returns_registered_tool() -> None:
    registry = AgentRegistry()
    registry.register(_FakeAgent("agent_a", ["tool_1"]))
    tool = registry.get_tool("tool_1")
    assert tool.name == "tool_1"
