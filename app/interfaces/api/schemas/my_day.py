from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.domain.entities import FocusExitReason, FocusStuckReason, TaskImportance


class GoalView(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime


class CreateGoalRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class UpdateGoalRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)


class DailyTaskPickRequest(BaseModel):
    task_id: uuid.UUID
    deliverable: str = Field(..., min_length=1)
    estimated_minutes: int = Field(..., gt=0)
    importance: TaskImportance
    goal_id: uuid.UUID | None = None


class SelectDailyTasksRequest(BaseModel):
    main: DailyTaskPickRequest
    secondary: list[DailyTaskPickRequest] = Field(default_factory=list, max_length=2)


class SwapDailyTaskRequest(BaseModel):
    bumped_task_id: uuid.UUID
    pick: DailyTaskPickRequest


class DailyPlanView(BaseModel):
    id: uuid.UUID
    plan_date: date
    main_task_id: uuid.UUID | None
    secondary_task_id_1: uuid.UUID | None
    secondary_task_id_2: uuid.UUID | None
    is_locked: bool
    locked_at: datetime | None
    carry_over_task_id: uuid.UUID | None
    created_at: datetime
    updated_at: datetime


class QuickCaptureTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)


class SetNextStepRequest(BaseModel):
    next_step: str | None = None


class StartFocusRequest(BaseModel):
    task_id: uuid.UUID


class EndFocusRequest(BaseModel):
    exit_reason: FocusExitReason
    stuck_reason: FocusStuckReason | None = None


class FocusSessionView(BaseModel):
    id: uuid.UUID
    task_id: uuid.UUID
    daily_plan_id: uuid.UUID
    started_at: datetime
    ended_at: datetime | None
    exit_reason: FocusExitReason | None
    stuck_reason: FocusStuckReason | None


class CarryOverRequest(BaseModel):
    task_id: uuid.UUID | None = None


class EndOfDaySummaryView(BaseModel):
    plan_date: date
    main_task_completed: bool
    completed_tasks: list[str]
    incomplete_tasks: list[str]
    stuck_reason_counts: dict[str, int]
    swap_count: int
    carry_over_task_id: uuid.UUID | None


class DailyPlanMetricsView(BaseModel):
    from_date: date
    to_date: date
    main_task_completion_rate: float
    focus_blocks_completed: int
    avg_estimated_minutes: float
    avg_actual_minutes: float
    urgent_swaps_total: int
