from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import AgentExecution


class AgentExecutionRepositoryPort(ABC):
    """Audit log of every tool invocation, for enterprise traceability."""

    @abstractmethod
    async def record(self, execution: AgentExecution) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_recent(self, user_id: uuid.UUID, limit: int = 10) -> list[AgentExecution]:
        """Most recent executions first — backs the dashboard's activity feed."""
        raise NotImplementedError
