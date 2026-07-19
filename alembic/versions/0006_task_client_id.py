"""task client_id

Revision ID: 0006
Revises: 0005
Create Date: 2026-07-19

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column(
            "client_id", sa.Uuid(), sa.ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
        ),
    )
    op.create_index("ix_tasks_client_id", "tasks", ["client_id"])


def downgrade() -> None:
    op.drop_index("ix_tasks_client_id", table_name="tasks")
    op.drop_column("tasks", "client_id")
