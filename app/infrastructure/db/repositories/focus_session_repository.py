from __future__ import annotations

import uuid
from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.focus_session_repository import FocusSessionRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import FocusExitReason, FocusSession, FocusStuckReason
from app.infrastructure.db.models import FocusSessionModel


class SqlAlchemyFocusSessionRepository(FocusSessionRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def start(
        self, user_id: uuid.UUID, task_id: uuid.UUID, daily_plan_id: uuid.UUID
    ) -> FocusSession:
        row = FocusSessionModel(user_id=user_id, task_id=task_id, daily_plan_id=daily_plan_id)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def end(
        self,
        session_id: uuid.UUID,
        exit_reason: FocusExitReason,
        stuck_reason: FocusStuckReason | None,
    ) -> FocusSession:
        row = await self._session.get(FocusSessionModel, session_id)
        if row is None:
            raise NotFoundError("Focus session not found", details={"session_id": str(session_id)})
        row.ended_at = datetime.now(UTC)
        row.exit_reason = exit_reason.value
        row.stuck_reason = stuck_reason.value if stuck_reason else None
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def get(self, session_id: uuid.UUID) -> FocusSession | None:
        row = await self._session.get(FocusSessionModel, session_id)
        return self._to_entity(row) if row else None

    async def get_active_by_user(self, user_id: uuid.UUID) -> FocusSession | None:
        stmt = select(FocusSessionModel).where(
            FocusSessionModel.user_id == user_id, FocusSessionModel.ended_at.is_(None)
        )
        row = (await self._session.scalars(stmt)).first()
        return self._to_entity(row) if row else None

    async def list_by_daily_plan(self, daily_plan_id: uuid.UUID) -> list[FocusSession]:
        stmt = select(FocusSessionModel).where(
            FocusSessionModel.daily_plan_id == daily_plan_id
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    async def list_by_user_between(
        self, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[FocusSession]:
        stmt = select(FocusSessionModel).where(
            FocusSessionModel.user_id == user_id,
            FocusSessionModel.started_at >= start_date,
            FocusSessionModel.started_at < end_date,
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row: FocusSessionModel) -> FocusSession:
        return FocusSession(
            id=row.id,
            user_id=row.user_id,
            task_id=row.task_id,
            daily_plan_id=row.daily_plan_id,
            started_at=row.started_at,
            ended_at=row.ended_at,
            exit_reason=FocusExitReason(row.exit_reason) if row.exit_reason else None,
            stuck_reason=FocusStuckReason(row.stuck_reason) if row.stuck_reason else None,
        )
