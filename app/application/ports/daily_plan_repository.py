from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import date

from app.domain.entities import DailyPlan


class DailyPlanRepositoryPort(ABC):
    @abstractmethod
    async def get_by_date(self, user_id: uuid.UUID, plan_date: date) -> DailyPlan | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, user_id: uuid.UUID, plan_date: date) -> DailyPlan:
        raise NotImplementedError

    @abstractmethod
    async def get(self, daily_plan_id: uuid.UUID) -> DailyPlan | None:
        raise NotImplementedError

    @abstractmethod
    async def set_main_task(
        self, daily_plan_id: uuid.UUID, task_id: uuid.UUID | None
    ) -> DailyPlan:
        raise NotImplementedError

    @abstractmethod
    async def set_secondary_task(
        self, daily_plan_id: uuid.UUID, slot: int, task_id: uuid.UUID | None
    ) -> DailyPlan:
        """`slot` is `1` or `2` — selects `secondary_task_id_1`/`_2`."""
        raise NotImplementedError

    @abstractmethod
    async def lock(self, daily_plan_id: uuid.UUID) -> DailyPlan:
        raise NotImplementedError

    @abstractmethod
    async def set_carry_over(
        self, daily_plan_id: uuid.UUID, task_id: uuid.UUID | None
    ) -> DailyPlan:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_between(
        self, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[DailyPlan]:
        """Inclusive of `start_date`, exclusive of `end_date` — used for metrics."""
        raise NotImplementedError
