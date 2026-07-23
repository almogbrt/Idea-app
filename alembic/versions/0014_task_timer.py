"""task timer

Revision ID: 0014
Revises: 0013
Create Date: 2026-07-23

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0014"
down_revision: str | None = "0013"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "tasks", sa.Column("timer_started_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("tasks", "timer_started_at")
