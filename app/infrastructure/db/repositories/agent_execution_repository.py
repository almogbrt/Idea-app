from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.agent_execution_repository import AgentExecutionRepositoryPort
from app.domain.entities import AgentExecution, ExecutionStatus
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

    async def list_recent(self, user_id: uuid.UUID, limit: int = 10) -> list[AgentExecution]:
        stmt = (
            select(AgentExecutionModel)
            .where(AgentExecutionModel.user_id == user_id)
            .order_by(AgentExecutionModel.created_at.desc())
            .limit(limit)
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row: AgentExecutionModel) -> AgentExecution:
        return AgentExecution(
            id=row.id,
            user_id=row.user_id,
            agent_name=row.agent_name,
            tool_name=row.tool_name,
            input=row.input,
            output=row.output,
            status=ExecutionStatus(row.status),
            latency_ms=row.latency_ms,
            created_at=row.created_at,
        )
