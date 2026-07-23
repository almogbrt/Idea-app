from __future__ import annotations

import uuid
from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.daily_plan_repository import DailyPlanRepositoryPort
from app.core.exceptions import NotFoundError, ValidationError
from app.domain.entities import DailyPlan
from app.infrastructure.db.models import DailyPlanModel


class SqlAlchemyDailyPlanRepository(DailyPlanRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_date(self, user_id: uuid.UUID, plan_date: date) -> DailyPlan | None:
        stmt = select(DailyPlanModel).where(
            DailyPlanModel.user_id == user_id, DailyPlanModel.plan_date == plan_date
        )
        row = (await self._session.scalars(stmt)).first()
        return self._to_entity(row) if row else None

    async def create(self, user_id: uuid.UUID, plan_date: date) -> DailyPlan:
        row = DailyPlanModel(user_id=user_id, plan_date=plan_date)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def get(self, daily_plan_id: uuid.UUID) -> DailyPlan | None:
        row = await self._session.get(DailyPlanModel, daily_plan_id)
        return self._to_entity(row) if row else None

    async def set_main_task(
        self, daily_plan_id: uuid.UUID, task_id: uuid.UUID | None
    ) -> DailyPlan:
        row = await self._get_or_raise(daily_plan_id)
        row.main_task_id = task_id
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def set_secondary_task(
        self, daily_plan_id: uuid.UUID, slot: int, task_id: uuid.UUID | None
    ) -> DailyPlan:
        row = await self._get_or_raise(daily_plan_id)
        if slot == 1:
            row.secondary_task_id_1 = task_id
        elif slot == 2:
            row.secondary_task_id_2 = task_id
        else:
            raise ValidationError("slot must be 1 or 2", details={"slot": slot})
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def lock(self, daily_plan_id: uuid.UUID) -> DailyPlan:
        row = await self._get_or_raise(daily_plan_id)
        row.is_locked = True
        row.locked_at = datetime.now(UTC)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def set_carry_over(
        self, daily_plan_id: uuid.UUID, task_id: uuid.UUID | None
    ) -> DailyPlan:
        row = await self._get_or_raise(daily_plan_id)
        row.carry_over_task_id = task_id
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def list_by_user_between(
        self, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[DailyPlan]:
        stmt = select(DailyPlanModel).where(
            DailyPlanModel.user_id == user_id,
            DailyPlanModel.plan_date >= start_date,
            DailyPlanModel.plan_date < end_date,
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._to_entity(row) for row in rows]

    async def _get_or_raise(self, daily_plan_id: uuid.UUID) -> DailyPlanModel:
        row = await self._session.get(DailyPlanModel, daily_plan_id)
        if row is None:
            raise NotFoundError(
                "Daily plan not found", details={"daily_plan_id": str(daily_plan_id)}
            )
        return row

    @staticmethod
    def _to_entity(row: DailyPlanModel) -> DailyPlan:
        return DailyPlan(
            id=row.id,
            user_id=row.user_id,
            plan_date=row.plan_date,
            main_task_id=row.main_task_id,
            secondary_task_id_1=row.secondary_task_id_1,
            secondary_task_id_2=row.secondary_task_id_2,
            is_locked=row.is_locked,
            locked_at=row.locked_at,
            carry_over_task_id=row.carry_over_task_id,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
