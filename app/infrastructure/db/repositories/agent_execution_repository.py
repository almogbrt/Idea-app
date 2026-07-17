from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.agent_execution_repository import AgentExecutionRepositoryPort
from app.domain.entities import AgentExecution
from app.infrastructure.db.models import AgentExecutionModel


class SqlAlchemyAgentExecutionRepository(AgentExecutionRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def record(self, execution: AgentExecution) -> None:
        row = AgentExecutionModel(
            id=execution.id,
            user_id=execution.user_id,
            agent_name=execution.agent_name,
            tool_name=execution.tool_name,
            input=execution.input,
            output=execution.output,
            status=execution.status.value,
            latency_ms=execution.latency_ms,
        )
        self._session.add(row)
        await self._session.flush()
