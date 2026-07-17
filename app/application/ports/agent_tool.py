"""Port that every Agent's tools implement, and that the orchestrator consumes.

This is the seam that makes the system extensible: `AgentRegistry` (in
`app/orchestrator/agent_registry.py`) only ever talks to `Tool`. A brand new
agent is just a new module that constructs `Tool` instances and registers
them — nothing in the orchestrator or intent router changes.
"""

from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from app.domain.entities import ToolDefinition, ToolResult


@dataclass(frozen=True, slots=True)
class ToolExecutionContext:
    """Per-call context threaded into every tool execution for auditability."""

    user_id: uuid.UUID
    conversation_id: uuid.UUID
    correlation_id: str


class Tool(ABC):
    """A single, independently invocable capability exposed by an Agent."""

    name: str
    description: str
    parameters_schema: dict[str, Any]
    agent_name: str

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            parameters_schema=self.parameters_schema,
            agent_name=self.agent_name,
        )

    @abstractmethod
    async def execute(
        self, arguments: dict[str, Any], context: ToolExecutionContext
    ) -> ToolResult:
        raise NotImplementedError
