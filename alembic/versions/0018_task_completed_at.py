"""task completed_at

Revision ID: 0018
Revises: 0017
Create Date: 2026-07-26

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0018"
down_revision: str | None = "0017"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True))
    # Best-effort backfill: for tasks already marked done before this column
    # existed, `updated_at` is the closest proxy we have for "when it was
    # finished" (nothing more precise was ever recorded).
    op.execute("UPDATE tasks SET completed_at = updated_at WHERE status = 'done'")


def downgrade() -> None:
    op.drop_column("tasks", "completed_at")
