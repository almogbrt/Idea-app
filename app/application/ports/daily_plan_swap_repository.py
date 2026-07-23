from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import date

from app.domain.entities import DailyPlanSwap


class DailyPlanSwapRepositoryPort(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: uuid.UUID,
        daily_plan_id: uuid.UUID,
        bumped_task_id: uuid.UUID,
        new_task_id: uuid.UUID,
    ) -> DailyPlanSwap:
        raise NotImplementedError

    @abstractmethod
    async def list_by_daily_plan(self, daily_plan_id: uuid.UUID) -> list[DailyPlanSwap]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_between(
        self, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[DailyPlanSwap]:
        raise NotImplementedError
