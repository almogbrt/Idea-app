from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from datetime import date

from app.domain.entities import FocusExitReason, FocusSession, FocusStuckReason


class FocusSessionRepositoryPort(ABC):
    @abstractmethod
    async def start(
        self, user_id: uuid.UUID, task_id: uuid.UUID, daily_plan_id: uuid.UUID
    ) -> FocusSession:
        raise NotImplementedError

    @abstractmethod
    async def end(
        self,
        session_id: uuid.UUID,
        exit_reason: FocusExitReason,
        stuck_reason: FocusStuckReason | None,
    ) -> FocusSession:
        raise NotImplementedError

    @abstractmethod
    async def get(self, session_id: uuid.UUID) -> FocusSession | None:
        raise NotImplementedError

    @abstractmethod
    async def get_active_by_user(self, user_id: uuid.UUID) -> FocusSession | None:
        """The session with `ended_at IS NULL` for this user, if any."""
        raise NotImplementedError

    @abstractmethod
    async def list_by_daily_plan(self, daily_plan_id: uuid.UUID) -> list[FocusSession]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user_between(
        self, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[FocusSession]:
        """By `started_at` date, inclusive of `start_date`, exclusive of `end_date`."""
        raise NotImplementedError
