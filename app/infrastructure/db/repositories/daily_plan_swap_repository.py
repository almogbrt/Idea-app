from __future__ import annotations

import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.daily_plan_swap_repository import DailyPlanSwapRepositoryPort
from app.domain.entities import DailyPlanSwap
from app.infrastructure.db.models import DailyPlanSwapModel


class SqlAlchemyDailyPlanSwapRepository(DailyPlanSwapRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: uuid.UUID,
        daily_plan_id: uuid.UUID,
        bumped_task_id: uuid.UUID,
        new_task_id: uuid.UUID,
    ) -> DailyPlanSwap:
        row = DailyPlanSwapModel(
            user_id=user_id,
            daily_plan_id=daily_plan_id,
            bumped_task_id=bumped_task_id,
            new_task_id=new_task_id,
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def list_by_daily_plan(self, daily_plan_id: uuid.UUID) -> list[DailyPlanSwap]:
        stmt = select(DailyPlanSwapModel).where(
            DailyPlanSwapModel.daily_plan_id == daily_plan_id
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    async def list_by_user_between(
        self, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[DailyPlanSwap]:
        stmt = select(DailyPlanSwapModel).where(
            DailyPlanSwapModel.user_id == user_id,
            DailyPlanSwapModel.created_at >= start_date,
            DailyPlanSwapModel.created_at < end_date,
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    @staticmethod
    def _to_entity(row: DailyPlanSwapModel) -> DailyPlanSwap:
        return DailyPlanSwap(
            id=row.id,
            user_id=row.user_id,
            daily_plan_id=row.daily_plan_id,
            bumped_task_id=row.bumped_task_id,
            new_task_id=row.new_task_id,
            created_at=row.created_at,
        )
