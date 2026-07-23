"""my day

Revision ID: 0015
Revises: 0014
Create Date: 2026-07-23

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0015"
down_revision: str | None = "0014"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "goals",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_goals_user_id", "goals", ["user_id"])

    op.add_column("tasks", sa.Column("deliverable", sa.Text(), nullable=True))
    op.add_column("tasks", sa.Column("estimated_minutes", sa.Integer(), nullable=True))
    op.add_column("tasks", sa.Column("importance", sa.String(20), nullable=True))
    op.add_column(
        "tasks",
        sa.Column(
            "goal_id",
            sa.Uuid(),
            sa.ForeignKey("goals.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.add_column("tasks", sa.Column("next_step", sa.Text(), nullable=True))

    op.create_table(
        "daily_plans",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("plan_date", sa.Date(), nullable=False),
        sa.Column(
            "main_task_id", sa.Uuid(), sa.ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column(
            "secondary_task_id_1",
            sa.Uuid(),
            sa.ForeignKey("tasks.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "secondary_task_id_2",
            sa.Uuid(),
            sa.ForeignKey("tasks.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("is_locked", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("locked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "carry_over_task_id",
            sa.Uuid(),
            sa.ForeignKey("tasks.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.UniqueConstraint("user_id", "plan_date", name="uq_daily_plans_user_id_plan_date"),
    )
    op.create_index("ix_daily_plans_user_id", "daily_plans", ["user_id"])

    op.create_table(
        "focus_sessions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "task_id", sa.Uuid(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "daily_plan_id",
            sa.Uuid(),
            sa.ForeignKey("daily_plans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("exit_reason", sa.String(20), nullable=True),
        sa.Column("stuck_reason", sa.String(20), nullable=True),
    )
    op.create_index("ix_focus_sessions_user_id", "focus_sessions", ["user_id"])
    op.create_index("ix_focus_sessions_daily_plan_id", "focus_sessions", ["daily_plan_id"])

    op.create_table(
        "daily_plan_swaps",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "daily_plan_id",
            sa.Uuid(),
            sa.ForeignKey("daily_plans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "bumped_task_id",
            sa.Uuid(),
            sa.ForeignKey("tasks.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "new_task_id", sa.Uuid(), sa.ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_daily_plan_swaps_daily_plan_id", "daily_plan_swaps", ["daily_plan_id"])


def downgrade() -> None:
    op.drop_index("ix_daily_plan_swaps_daily_plan_id", table_name="daily_plan_swaps")
    op.drop_table("daily_plan_swaps")

    op.drop_index("ix_focus_sessions_daily_plan_id", table_name="focus_sessions")
    op.drop_index("ix_focus_sessions_user_id", table_name="focus_sessions")
    op.drop_table("focus_sessions")

    op.drop_index("ix_daily_plans_user_id", table_name="daily_plans")
    op.drop_table("daily_plans")

    op.drop_column("tasks", "next_step")
    op.drop_column("tasks", "goal_id")
    op.drop_column("tasks", "importance")
    op.drop_column("tasks", "estimated_minutes")
    op.drop_column("tasks", "deliverable")

    op.drop_index("ix_goals_user_id", table_name="goals")
    op.drop_table("goals")
