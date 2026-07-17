from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.entities import AgentExecution


class AgentExecutionRepositoryPort(ABC):
    """Audit log of every tool invocation, for enterprise traceability."""

    @abstractmethod
    async def record(self, execution: AgentExecution) -> None:
        raise NotImplementedError
