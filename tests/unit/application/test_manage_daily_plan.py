from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

from app.application.use_cases.manage_daily_plan import (
    DailyPlanMetricsUseCase,
    DailyTaskPick,
    ManageDailyPlanUseCase,
    ManageFocusSessionUseCase,
    ManageGoalsUseCase,
)
from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.domain.entities import FocusExitReason, FocusStuckReason, TaskImportance, TaskStatus
from tests.conftest import (
    FakeDailyPlanRepository,
    FakeDailyPlanSwapRepository,
    FakeFocusSessionRepository,
    FakeGoalRepository,
    FakeTaskRepository,
)


def _pick(task_id: uuid.UUID, **overrides: object) -> DailyTaskPick:
    defaults: dict[str, object] = {
        "deliverable": "A finished draft",
        "estimated_minutes": 60,
        "importance": TaskImportance.HIGH,
        "goal_id": None,
    }
    defaults.update(overrides)
    return DailyTaskPick(task_id=task_id, **defaults)  # type: ignore[arg-type]


async def test_goals_create_list_update_delete(
    fake_goal_repository: FakeGoalRepository,
) -> None:
    use_case = ManageGoalsUseCase(fake_goal_repository)
    user_id = uuid.uuid4()

    goal = await use_case.create(user_id, "  Grow the business  ")
    assert goal.name == "Grow the business"

    goals = await use_case.list_all(user_id)
    assert [g.id for g in goals] == [goal.id]

    updated = await use_case.update(goal.id, "Grow the business 2x")
    assert updated.name == "Grow the business 2x"

    await use_case.delete(goal.id)
    assert await use_case.list_all(user_id) == []


async def test_goals_create_rejects_blank_name(fake_goal_repository: FakeGoalRepository) -> None:
    use_case = ManageGoalsUseCase(fake_goal_repository)
    with pytest.raises(ValidationError):
        await use_case.create(uuid.uuid4(), "   ")


async def test_goals_get_or_raise_missing(fake_goal_repository: FakeGoalRepository) -> None:
    use_case = ManageGoalsUseCase(fake_goal_repository)
    with pytest.raises(NotFoundError):
        await use_case.get_or_raise(uuid.uuid4())


def _daily_plan_use_case(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> ManageDailyPlanUseCase:
    return ManageDailyPlanUseCase(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )


async def test_select_daily_tasks_sets_main_and_secondary(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    secondary_task = await fake_task_repository.create(user_id, "Secondary task")

    plan = await use_case.select_daily_tasks(
        user_id, _pick(main_task.id), [_pick(secondary_task.id)]
    )

    assert plan.main_task_id == main_task.id
    assert plan.secondary_task_id_1 == secondary_task.id
    assert plan.secondary_task_id_2 is None
    updated_main = await fake_task_repository.get(main_task.id)
    assert updated_main is not None
    assert updated_main.deliverable == "A finished draft"
    assert updated_main.importance == TaskImportance.HIGH


async def test_select_daily_tasks_rejects_more_than_two_secondary(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    extra_tasks = [await fake_task_repository.create(user_id, f"Task {i}") for i in range(3)]

    with pytest.raises(ValidationError):
        await use_case.select_daily_tasks(
            user_id, _pick(main_task.id), [_pick(t.id) for t in extra_tasks]
        )


async def test_select_daily_tasks_rejected_after_lock(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    await use_case.select_daily_tasks(user_id, _pick(main_task.id), [])
    await use_case.lock_day(user_id)

    with pytest.raises(ConflictError):
        await use_case.select_daily_tasks(user_id, _pick(main_task.id), [])


async def test_lock_day_requires_a_main_task(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    with pytest.raises(ValidationError):
        await use_case.lock_day(uuid.uuid4())


async def test_swap_daily_task_requires_locked_plan(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    new_task = await fake_task_repository.create(user_id, "Urgent task")
    await use_case.select_daily_tasks(user_id, _pick(main_task.id), [])

    with pytest.raises(ValidationError):
        await use_case.swap_daily_task(user_id, main_task.id, _pick(new_task.id))


async def test_swap_daily_task_rejects_task_not_in_plan(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    not_in_plan = await fake_task_repository.create(user_id, "Not in plan")
    new_task = await fake_task_repository.create(user_id, "Urgent task")
    await use_case.select_daily_tasks(user_id, _pick(main_task.id), [])
    await use_case.lock_day(user_id)

    with pytest.raises(ValidationError):
        await use_case.swap_daily_task(user_id, not_in_plan.id, _pick(new_task.id))


async def test_swap_daily_task_replaces_slot_and_logs_swap(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    secondary_task = await fake_task_repository.create(user_id, "Secondary task")
    urgent_task = await fake_task_repository.create(user_id, "Urgent task")
    plan = await use_case.select_daily_tasks(
        user_id, _pick(main_task.id), [_pick(secondary_task.id)]
    )
    await use_case.lock_day(user_id)

    updated = await use_case.swap_daily_task(user_id, secondary_task.id, _pick(urgent_task.id))

    assert updated.secondary_task_id_1 == urgent_task.id
    swaps = await fake_daily_plan_swap_repository.list_by_daily_plan(plan.id)
    assert len(swaps) == 1
    assert swaps[0].bumped_task_id == secondary_task.id
    assert swaps[0].new_task_id == urgent_task.id


async def test_set_carry_over(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    user_id = uuid.uuid4()
    task = await fake_task_repository.create(user_id, "Tomorrow's first task")

    plan = await use_case.set_carry_over(user_id, task.id)

    assert plan.carry_over_task_id == task.id


async def test_start_focus_requires_locked_plan(
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    use_case = ManageFocusSessionUseCase(fake_focus_session_repository, fake_daily_plan_repository)
    user_id = uuid.uuid4()
    task = await fake_task_repository.create(user_id, "Task")

    with pytest.raises(ValidationError):
        await use_case.start_focus(user_id, task.id)


async def test_start_focus_rejects_task_not_in_todays_plan(
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    plan_use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    focus_use_case = ManageFocusSessionUseCase(
        fake_focus_session_repository, fake_daily_plan_repository
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    other_task = await fake_task_repository.create(user_id, "Not in plan")
    await plan_use_case.select_daily_tasks(user_id, _pick(main_task.id), [])
    await plan_use_case.lock_day(user_id)

    with pytest.raises(ValidationError):
        await focus_use_case.start_focus(user_id, other_task.id)


async def test_start_focus_happy_path_and_idempotent_resume(
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    plan_use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    focus_use_case = ManageFocusSessionUseCase(
        fake_focus_session_repository, fake_daily_plan_repository
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    await plan_use_case.select_daily_tasks(user_id, _pick(main_task.id), [])
    await plan_use_case.lock_day(user_id)

    session = await focus_use_case.start_focus(user_id, main_task.id)
    assert session.ended_at is None

    resumed = await focus_use_case.start_focus(user_id, main_task.id)
    assert resumed.id == session.id


async def test_start_focus_conflicts_with_a_different_active_task(
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    plan_use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    focus_use_case = ManageFocusSessionUseCase(
        fake_focus_session_repository, fake_daily_plan_repository
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    secondary_task = await fake_task_repository.create(user_id, "Secondary task")
    await plan_use_case.select_daily_tasks(
        user_id, _pick(main_task.id), [_pick(secondary_task.id)]
    )
    await plan_use_case.lock_day(user_id)
    await focus_use_case.start_focus(user_id, main_task.id)

    with pytest.raises(ConflictError):
        await focus_use_case.start_focus(user_id, secondary_task.id)


async def test_end_focus_stuck_requires_stuck_reason(
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
) -> None:
    use_case = ManageFocusSessionUseCase(fake_focus_session_repository, fake_daily_plan_repository)
    session = await fake_focus_session_repository.start(uuid.uuid4(), uuid.uuid4(), uuid.uuid4())

    with pytest.raises(ValidationError):
        await use_case.end_focus(session.id, FocusExitReason.STUCK, None)


async def test_end_focus_non_stuck_rejects_stuck_reason(
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
) -> None:
    use_case = ManageFocusSessionUseCase(fake_focus_session_repository, fake_daily_plan_repository)
    session = await fake_focus_session_repository.start(uuid.uuid4(), uuid.uuid4(), uuid.uuid4())

    with pytest.raises(ValidationError):
        await use_case.end_focus(session.id, FocusExitReason.DONE, FocusStuckReason.TOO_BIG)


async def test_end_focus_happy_path(
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
) -> None:
    use_case = ManageFocusSessionUseCase(fake_focus_session_repository, fake_daily_plan_repository)
    session = await fake_focus_session_repository.start(uuid.uuid4(), uuid.uuid4(), uuid.uuid4())

    ended = await use_case.end_focus(session.id, FocusExitReason.DONE, None)

    assert ended.ended_at is not None
    assert ended.exit_reason == FocusExitReason.DONE
    assert await fake_focus_session_repository.get_active_by_user(session.user_id) is None


async def test_get_or_raise_missing_focus_session(
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_daily_plan_repository: FakeDailyPlanRepository,
) -> None:
    use_case = ManageFocusSessionUseCase(fake_focus_session_repository, fake_daily_plan_repository)
    with pytest.raises(NotFoundError):
        await use_case.get_or_raise(uuid.uuid4())


async def test_end_of_day_summary_aggregates_completed_incomplete_stuck_and_swaps(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    plan_use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    metrics_use_case = DailyPlanMetricsUseCase(
        fake_daily_plan_repository,
        fake_focus_session_repository,
        fake_daily_plan_swap_repository,
        fake_task_repository,
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    secondary_task = await fake_task_repository.create(user_id, "Secondary task")
    plan = await plan_use_case.select_daily_tasks(
        user_id, _pick(main_task.id), [_pick(secondary_task.id)]
    )
    await plan_use_case.lock_day(user_id)
    await fake_task_repository.update_status(main_task.id, TaskStatus.DONE)

    session = await fake_focus_session_repository.start(user_id, secondary_task.id, plan.id)
    await fake_focus_session_repository.end(
        session.id, FocusExitReason.STUCK, FocusStuckReason.DISTRACTED
    )
    await fake_daily_plan_swap_repository.create(
        user_id, plan.id, secondary_task.id, main_task.id
    )

    summary = await metrics_use_case.end_of_day_summary(user_id, plan.plan_date)

    assert summary.main_task_completed is True
    assert summary.completed_task_titles == ["Main task"]
    assert summary.incomplete_task_titles == ["Secondary task"]
    assert summary.stuck_reason_counts == {FocusStuckReason.DISTRACTED: 1}
    assert summary.swap_count == 1


async def test_get_metrics_aggregates_across_date_range(
    fake_daily_plan_repository: FakeDailyPlanRepository,
    fake_daily_plan_swap_repository: FakeDailyPlanSwapRepository,
    fake_focus_session_repository: FakeFocusSessionRepository,
    fake_task_repository: FakeTaskRepository,
) -> None:
    plan_use_case = _daily_plan_use_case(
        fake_daily_plan_repository, fake_daily_plan_swap_repository, fake_task_repository
    )
    metrics_use_case = DailyPlanMetricsUseCase(
        fake_daily_plan_repository,
        fake_focus_session_repository,
        fake_daily_plan_swap_repository,
        fake_task_repository,
    )
    user_id = uuid.uuid4()
    main_task = await fake_task_repository.create(user_id, "Main task")
    plan = await plan_use_case.select_daily_tasks(
        user_id, _pick(main_task.id, estimated_minutes=30), []
    )
    await plan_use_case.lock_day(user_id)
    await fake_task_repository.update_status(main_task.id, TaskStatus.DONE)

    session = await fake_focus_session_repository.start(user_id, main_task.id, plan.id)
    session.started_at = datetime.now(UTC) - timedelta(minutes=45)
    await fake_focus_session_repository.end(session.id, FocusExitReason.DONE, None)

    today = plan.plan_date
    metrics = await metrics_use_case.get_metrics(
        user_id, today, today + timedelta(days=1)
    )

    assert metrics.main_task_completion_rate == 1.0
    assert metrics.focus_blocks_completed == 1
    assert metrics.avg_estimated_minutes == 30.0
    assert metrics.avg_actual_minutes == pytest.approx(45.0, abs=1.0)
    assert metrics.urgent_swaps_total == 0
