"""Use cases behind "היום שלי" (My Day): picking up to 3 daily outcomes,
locking the day, running distraction-free Focus sessions on them, swapping
in an urgent task mid-day, and reporting the day's accountability summary
and rolling metrics.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, date, datetime

from app.application.ports.daily_plan_repository import DailyPlanRepositoryPort
from app.application.ports.daily_plan_swap_repository import DailyPlanSwapRepositoryPort
from app.application.ports.focus_session_repository import FocusSessionRepositoryPort
from app.application.ports.goal_repository import GoalRepositoryPort
from app.application.ports.task_repository import TaskRepositoryPort
from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.domain.entities import (
    DailyPlan,
    FocusExitReason,
    FocusSession,
    FocusStuckReason,
    Goal,
    Task,
    TaskImportance,
    TaskStatus,
)


class ManageGoalsUseCase:
    def __init__(self, goal_repository: GoalRepositoryPort) -> None:
        self._goals = goal_repository

    async def create(self, user_id: uuid.UUID, name: str) -> Goal:
        stripped = name.strip()
        if not stripped:
            raise ValidationError("A goal needs a name.")
        return await self._goals.create(user_id, stripped)

    async def list_all(self, user_id: uuid.UUID) -> list[Goal]:
        return await self._goals.list_by_user(user_id)

    async def update(self, goal_id: uuid.UUID, name: str) -> Goal:
        stripped = name.strip()
        if not stripped:
            raise ValidationError("A goal needs a name.")
        return await self._goals.update(goal_id, stripped)

    async def delete(self, goal_id: uuid.UUID) -> None:
        await self._goals.delete(goal_id)

    async def get_or_raise(self, goal_id: uuid.UUID) -> Goal:
        goal = await self._goals.get(goal_id)
        if goal is None:
            raise NotFoundError("Goal not found", details={"goal_id": str(goal_id)})
        return goal


@dataclass(frozen=True, slots=True)
class DailyTaskPick:
    """Bundles the per-slot attributes collected when a task is picked as
    one of a day's 3 outcomes — an application-layer input, not a domain
    entity."""

    task_id: uuid.UUID
    deliverable: str
    estimated_minutes: int
    importance: TaskImportance
    goal_id: uuid.UUID | None


class ManageDailyPlanUseCase:
    def __init__(
        self,
        daily_plan_repository: DailyPlanRepositoryPort,
        daily_plan_swap_repository: DailyPlanSwapRepositoryPort,
        task_repository: TaskRepositoryPort,
    ) -> None:
        self._plans = daily_plan_repository
        self._swaps = daily_plan_swap_repository
        self._tasks = task_repository

    async def get_or_create_today(self, user_id: uuid.UUID) -> DailyPlan:
        today = datetime.now(UTC).date()
        plan = await self._plans.get_by_date(user_id, today)
        if plan is not None:
            return plan
        return await self._plans.create(user_id, today)

    async def select_daily_tasks(
        self, user_id: uuid.UUID, main: DailyTaskPick, secondary: list[DailyTaskPick]
    ) -> DailyPlan:
        if len(secondary) > 2:
            raise ValidationError(
                "At most 2 secondary tasks are allowed.", details={"count": len(secondary)}
            )
        plan = await self.get_or_create_today(user_id)
        if plan.is_locked:
            raise ConflictError("Today's plan is already locked.")

        await self._apply_pick(main)
        plan = await self._plans.set_main_task(plan.id, main.task_id)

        for slot, pick in enumerate(secondary, start=1):
            await self._apply_pick(pick)
            plan = await self._plans.set_secondary_task(plan.id, slot, pick.task_id)
        for slot in range(len(secondary) + 1, 3):
            plan = await self._plans.set_secondary_task(plan.id, slot, None)
        return plan

    async def _apply_pick(self, pick: DailyTaskPick) -> Task:
        return await self._tasks.set_daily_attributes(
            pick.task_id, pick.deliverable, pick.estimated_minutes, pick.importance, pick.goal_id
        )

    async def lock_day(self, user_id: uuid.UUID) -> DailyPlan:
        plan = await self.get_or_create_today(user_id)
        if plan.main_task_id is None:
            raise ValidationError("Pick a main task before locking the day.")
        return await self._plans.lock(plan.id)

    async def swap_daily_task(
        self,
        user_id: uuid.UUID,
        bumped_task_id: uuid.UUID,
        pick: DailyTaskPick,
    ) -> DailyPlan:
        plan = await self.get_or_create_today(user_id)
        if not plan.is_locked:
            raise ValidationError("Today's plan must be locked before swapping tasks.")

        await self._apply_pick(pick)
        if plan.main_task_id == bumped_task_id:
            plan = await self._plans.set_main_task(plan.id, pick.task_id)
        elif plan.secondary_task_id_1 == bumped_task_id:
            plan = await self._plans.set_secondary_task(plan.id, 1, pick.task_id)
        elif plan.secondary_task_id_2 == bumped_task_id:
            plan = await self._plans.set_secondary_task(plan.id, 2, pick.task_id)
        else:
            raise ValidationError("That task isn't part of today's plan.")

        await self._swaps.create(user_id, plan.id, bumped_task_id, pick.task_id)
        return plan

    async def set_carry_over(self, user_id: uuid.UUID, task_id: uuid.UUID | None) -> DailyPlan:
        plan = await self.get_or_create_today(user_id)
        return await self._plans.set_carry_over(plan.id, task_id)


class ManageFocusSessionUseCase:
    def __init__(
        self,
        focus_session_repository: FocusSessionRepositoryPort,
        daily_plan_repository: DailyPlanRepositoryPort,
    ) -> None:
        self._sessions = focus_session_repository
        self._plans = daily_plan_repository

    async def start_focus(self, user_id: uuid.UUID, task_id: uuid.UUID) -> FocusSession:
        today = datetime.now(UTC).date()
        plan = await self._plans.get_by_date(user_id, today)
        if plan is None or not plan.is_locked:
            raise ValidationError("Lock today's plan before starting Focus mode.")
        if task_id not in {plan.main_task_id, plan.secondary_task_id_1, plan.secondary_task_id_2}:
            raise ValidationError("That task isn't part of today's plan.")

        active = await self._sessions.get_active_by_user(user_id)
        if active is not None:
            if active.task_id == task_id:
                return active
            raise ConflictError("Another Focus session is already active.")
        return await self._sessions.start(user_id, task_id, plan.id)

    async def end_focus(
        self,
        session_id: uuid.UUID,
        exit_reason: FocusExitReason,
        stuck_reason: FocusStuckReason | None,
    ) -> FocusSession:
        if exit_reason == FocusExitReason.STUCK and stuck_reason is None:
            raise ValidationError('A "stuck" reason is required when exiting as stuck.')
        if exit_reason != FocusExitReason.STUCK and stuck_reason is not None:
            raise ValidationError("A stuck reason only applies when exiting as stuck.")
        return await self._sessions.end(session_id, exit_reason, stuck_reason)

    async def get_active(self, user_id: uuid.UUID) -> FocusSession | None:
        return await self._sessions.get_active_by_user(user_id)

    async def get_or_raise(self, session_id: uuid.UUID) -> FocusSession:
        session = await self._sessions.get(session_id)
        if session is None:
            raise NotFoundError(
                "Focus session not found", details={"session_id": str(session_id)}
            )
        return session


@dataclass(frozen=True, slots=True)
class EndOfDaySummary:
    plan_date: date
    main_task_completed: bool
    completed_task_titles: list[str]
    incomplete_task_titles: list[str]
    stuck_reason_counts: dict[FocusStuckReason, int]
    swap_count: int
    carry_over_task_id: uuid.UUID | None


@dataclass(frozen=True, slots=True)
class DailyPlanMetrics:
    from_date: date
    to_date: date
    main_task_completion_rate: float
    focus_blocks_completed: int
    avg_estimated_minutes: float
    avg_actual_minutes: float
    urgent_swaps_total: int


class DailyPlanMetricsUseCase:
    def __init__(
        self,
        daily_plan_repository: DailyPlanRepositoryPort,
        focus_session_repository: FocusSessionRepositoryPort,
        daily_plan_swap_repository: DailyPlanSwapRepositoryPort,
        task_repository: TaskRepositoryPort,
    ) -> None:
        self._plans = daily_plan_repository
        self._sessions = focus_session_repository
        self._swaps = daily_plan_swap_repository
        self._tasks = task_repository

    async def end_of_day_summary(self, user_id: uuid.UUID, plan_date: date) -> EndOfDaySummary:
        plan = await self._plans.get_by_date(user_id, plan_date)
        if plan is None:
            raise NotFoundError(
                "No plan for that date", details={"plan_date": plan_date.isoformat()}
            )

        task_ids = [
            t
            for t in (plan.main_task_id, plan.secondary_task_id_1, plan.secondary_task_id_2)
            if t is not None
        ]
        tasks = [t for t in [await self._tasks.get(tid) for tid in task_ids] if t is not None]

        main_task = next((t for t in tasks if t.id == plan.main_task_id), None)
        main_task_completed = main_task is not None and main_task.status == TaskStatus.DONE
        completed = [t.title for t in tasks if t.status == TaskStatus.DONE]
        incomplete = [t.title for t in tasks if t.status != TaskStatus.DONE]

        sessions = await self._sessions.list_by_daily_plan(plan.id)
        stuck_counts: dict[FocusStuckReason, int] = {}
        for session in sessions:
            if session.exit_reason == FocusExitReason.STUCK and session.stuck_reason is not None:
                stuck_counts[session.stuck_reason] = stuck_counts.get(session.stuck_reason, 0) + 1

        swaps = await self._swaps.list_by_daily_plan(plan.id)

        return EndOfDaySummary(
            plan_date=plan_date,
            main_task_completed=main_task_completed,
            completed_task_titles=completed,
            incomplete_task_titles=incomplete,
            stuck_reason_counts=stuck_counts,
            swap_count=len(swaps),
            carry_over_task_id=plan.carry_over_task_id,
        )

    async def get_metrics(
        self, user_id: uuid.UUID, from_date: date, to_date: date
    ) -> DailyPlanMetrics:
        plans = await self._plans.list_by_user_between(user_id, from_date, to_date)
        plans_with_main = [p for p in plans if p.main_task_id is not None]
        completed_main = 0
        for plan in plans_with_main:
            task = await self._tasks.get(plan.main_task_id)  # type: ignore[arg-type]
            if task is not None and task.status == TaskStatus.DONE:
                completed_main += 1
        main_task_completion_rate = (
            completed_main / len(plans_with_main) if plans_with_main else 0.0
        )

        sessions = await self._sessions.list_by_user_between(user_id, from_date, to_date)
        ended_sessions = [s for s in sessions if s.ended_at is not None]
        focus_blocks_completed = sum(
            1 for s in ended_sessions if s.exit_reason == FocusExitReason.DONE
        )

        estimated_minutes: list[int] = []
        actual_minutes: list[float] = []
        for session in ended_sessions:
            task = await self._tasks.get(session.task_id)
            if task is not None and task.estimated_minutes is not None:
                estimated_minutes.append(task.estimated_minutes)
            if session.ended_at is not None:
                actual_minutes.append((session.ended_at - session.started_at).total_seconds() / 60)

        avg_estimated_minutes = (
            sum(estimated_minutes) / len(estimated_minutes) if estimated_minutes else 0.0
        )
        avg_actual_minutes = sum(actual_minutes) / len(actual_minutes) if actual_minutes else 0.0

        swaps = await self._swaps.list_by_user_between(user_id, from_date, to_date)

        return DailyPlanMetrics(
            from_date=from_date,
            to_date=to_date,
            main_task_completion_rate=main_task_completion_rate,
            focus_blocks_completed=focus_blocks_completed,
            avg_estimated_minutes=avg_estimated_minutes,
            avg_actual_minutes=avg_actual_minutes,
            urgent_swaps_total=len(swaps),
        )
