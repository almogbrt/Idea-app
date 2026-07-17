"""Base class every Agent implements.

An Agent is nothing more than a named bundle of `Tool`s. It has no
knowledge of the orchestrator, the LLM, or other agents — it only knows how
to talk to its own external system (Drive, Gmail, Calendar, Sheets, ...).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.application.ports.agent_tool import Tool


class BaseAgent(ABC):
    name: str
    description: str

    @abstractmethod
    def get_tools(self) -> list[Tool]:
        """Return every tool this agent exposes to the Intent Router."""
        raise NotImplementedError
