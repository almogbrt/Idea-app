""""היום שלי" (My Day) REST endpoints: goals, the daily 3-task plan, Focus
sessions, and the end-of-day summary/metrics. Goes straight to the use
cases, bypassing the LLM tool-call loop — same reasoning as `workspace.py`.
"""

from __future__ import annotations

import uuid
from datetime import UTC, date, datetime

from fastapi import APIRouter, Depends

from app.application.use_cases.manage_daily_plan import DailyTaskPick
from app.core.container import RequestScopedServices
from app.core.exceptions import ForbiddenError
from app.domain.entities import (
    DailyPlan,
    FocusExitReason,
    FocusSession,
    Goal,
    TaskStatus,
    User,
)
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from app.interfaces.api.schemas.my_day import (
    CreateGoalRequest,
    DailyPlanMetricsView,
    DailyPlanView,
    DailyTaskPickRequest,
    EndFocusRequest,
    EndOfDaySummaryView,
    FocusSessionView,
    GoalView,
    QuickCaptureTaskRequest,
    SelectDailyTasksRequest,
    SetNextStepRequest,
    StartFocusRequest,
    SwapDailyTaskRequest,
    UpdateGoalRequest,
)
from app.interfaces.api.schemas.workspace import TaskView
from app.interfaces.api.v1.workspace import _ensure_task_owned_by, _task_view

router = APIRouter(prefix="/my-day", tags=["my-day"])


def _ensure_goal_owned_by(goal: Goal, user: User) -> None:
    if goal.user_id != user.id:
        raise ForbiddenError("This goal does not belong to you.")


def _ensure_focus_session_owned_by(session: FocusSession, user: User) -> None:
    if session.user_id != user.id:
        raise ForbiddenError("This focus session does not belong to you.")


def _goal_view(goal: Goal) -> GoalView:
    return GoalView(id=goal.id, name=goal.name, created_at=goal.created_at)


def _daily_plan_view(plan: DailyPlan) -> DailyPlanView:
    return DailyPlanView(
        id=plan.id,
        plan_date=plan.plan_date,
        main_task_id=plan.main_task_id,
        secondary_task_id_1=plan.secondary_task_id_1,
        secondary_task_id_2=plan.secondary_task_id_2,
        is_locked=plan.is_locked,
        locked_at=plan.locked_at,
        carry_over_task_id=plan.carry_over_task_id,
        created_at=plan.created_at,
        updated_at=plan.updated_at,
    )


def _focus_session_view(session: FocusSession) -> FocusSessionView:
    return FocusSessionView(
        id=session.id,
        task_id=session.task_id,
        daily_plan_id=session.daily_plan_id,
        started_at=session.started_at,
        ended_at=session.ended_at,
        exit_reason=session.exit_reason,
        stuck_reason=session.stuck_reason,
    )


@router.post("/goals", response_model=GoalView)
async def create_goal(
    body: CreateGoalRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> GoalView:
    goal = await scope.manage_goals.create(user.id, body.name)
    return _goal_view(goal)


@router.get("/goals", response_model=list[GoalView])
async def list_goals(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> list[GoalView]:
    goals = await scope.manage_goals.list_all(user.id)
    return [_goal_view(g) for g in goals]


@router.patch("/goals/{goal_id}", response_model=GoalView)
async def update_goal(
    goal_id: uuid.UUID,
    body: UpdateGoalRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> GoalView:
    existing = await scope.manage_goals.get_or_raise(goal_id)
    _ensure_goal_owned_by(existing, user)
    goal = await scope.manage_goals.update(goal_id, body.name)
    return _goal_view(goal)


@router.delete("/goals/{goal_id}", status_code=204)
async def delete_goal(
    goal_id: uuid.UUID,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> None:
    existing = await scope.manage_goals.get_or_raise(goal_id)
    _ensure_goal_owned_by(existing, user)
    await scope.manage_goals.delete(goal_id)


@router.get("/plan/today", response_model=DailyPlanView)
async def get_today_plan(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> DailyPlanView:
    plan = await scope.manage_daily_plan.get_or_create_today(user.id)
    return _daily_plan_view(plan)


@router.post("/plan/today/select", response_model=DailyPlanView)
async def select_daily_tasks(
    body: SelectDailyTasksRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> DailyPlanView:
    main = DailyTaskPick(
        task_id=body.main.task_id,
        deliverable=body.main.deliverable,
        estimated_minutes=body.main.estimated_minutes,
        importance=body.main.importance,
        goal_id=body.main.goal_id,
        next_step=body.main.next_step,
    )
    secondary = [
        DailyTaskPick(
            task_id=p.task_id,
            deliverable=p.deliverable,
            estimated_minutes=p.estimated_minutes,
            importance=p.importance,
            goal_id=p.goal_id,
            next_step=p.next_step,
        )
        for p in body.secondary
    ]
    plan = await scope.manage_daily_plan.select_daily_tasks(user.id, main, secondary)
    return _daily_plan_view(plan)


@router.post("/plan/today/lock", response_model=DailyPlanView)
async def lock_day(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> DailyPlanView:
    plan = await scope.manage_daily_plan.lock_day(user.id)
    return _daily_plan_view(plan)


@router.post("/inbox", response_model=TaskView)
async def quick_capture_task(
    body: QuickCaptureTaskRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> TaskView:
    task = await scope.manage_tasks.quick_capture(user.id, body.title)
    return _task_view(task)


@router.patch("/tasks/{task_id}/next-step", response_model=TaskView)
async def set_task_next_step(
    task_id: uuid.UUID,
    body: SetNextStepRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> TaskView:
    existing = await scope.manage_tasks.get_or_raise(task_id)
    _ensure_task_owned_by(existing, user)
    task = await scope.manage_tasks.set_next_step(task_id, body.next_step)
    return _task_view(task)


@router.post("/plan/today/swap", response_model=DailyPlanView)
async def swap_daily_task(
    body: SwapDailyTaskRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> DailyPlanView:
    pick = DailyTaskPick(
        task_id=body.pick.task_id,
        deliverable=body.pick.deliverable,
        estimated_minutes=body.pick.estimated_minutes,
        importance=body.pick.importance,
        goal_id=body.pick.goal_id,
        next_step=body.pick.next_step,
    )
    plan = await scope.manage_daily_plan.swap_daily_task(user.id, body.bumped_task_id, pick)
    return _daily_plan_view(plan)


@router.post("/plan/tomorrow/first-task", response_model=DailyPlanView)
async def plan_tomorrows_first_task(
    body: DailyTaskPickRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> DailyPlanView:
    pick = DailyTaskPick(
        task_id=body.task_id,
        deliverable=body.deliverable,
        estimated_minutes=body.estimated_minutes,
        importance=body.importance,
        goal_id=body.goal_id,
        next_step=body.next_step,
    )
    plan = await scope.manage_daily_plan.plan_tomorrows_first_task(user.id, pick)
    return _daily_plan_view(plan)


@router.post("/focus/start", response_model=FocusSessionView)
async def start_focus(
    body: StartFocusRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> FocusSessionView:
    session = await scope.manage_focus_sessions.start_focus(user.id, body.task_id)
    return _focus_session_view(session)


@router.post("/focus/{session_id}/end", response_model=FocusSessionView)
async def end_focus(
    session_id: uuid.UUID,
    body: EndFocusRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> FocusSessionView:
    existing = await scope.manage_focus_sessions.get_or_raise(session_id)
    _ensure_focus_session_owned_by(existing, user)
    session = await scope.manage_focus_sessions.end_focus(
        session_id, body.exit_reason, body.stuck_reason
    )
    if body.exit_reason == FocusExitReason.DONE:
        await scope.manage_tasks.update_status(session.task_id, TaskStatus.DONE)
    return _focus_session_view(session)


@router.get("/focus/active", response_model=FocusSessionView | None)
async def get_active_focus(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> FocusSessionView | None:
    session = await scope.manage_focus_sessions.get_active(user.id)
    return _focus_session_view(session) if session else None


@router.get("/plan/today/summary", response_model=EndOfDaySummaryView)
async def get_today_summary(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> EndOfDaySummaryView:
    today = datetime.now(UTC).date()
    summary = await scope.daily_plan_metrics.end_of_day_summary(user.id, today)
    return EndOfDaySummaryView(
        plan_date=summary.plan_date,
        main_task_completed=summary.main_task_completed,
        completed_tasks=summary.completed_task_titles,
        incomplete_tasks=summary.incomplete_task_titles,
        stuck_reason_counts={k.value: v for k, v in summary.stuck_reason_counts.items()},
        swap_count=summary.swap_count,
        carry_over_task_id=summary.carry_over_task_id,
    )


@router.get("/metrics", response_model=DailyPlanMetricsView)
async def get_metrics(
    from_date: date,
    to_date: date,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> DailyPlanMetricsView:
    metrics = await scope.daily_plan_metrics.get_metrics(user.id, from_date, to_date)
    return DailyPlanMetricsView(
        from_date=metrics.from_date,
        to_date=metrics.to_date,
        main_task_completion_rate=metrics.main_task_completion_rate,
        focus_blocks_completed=metrics.focus_blocks_completed,
        avg_estimated_minutes=metrics.avg_estimated_minutes,
        avg_actual_minutes=metrics.avg_actual_minutes,
        urgent_swaps_total=metrics.urgent_swaps_total,
    )
