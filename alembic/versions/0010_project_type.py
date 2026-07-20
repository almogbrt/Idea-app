"""project type replaces status

Revision ID: 0010
Revises: 0009
Create Date: 2026-07-20

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010"
down_revision: str | None = "0009"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("projects", sa.Column("type", sa.String(20), nullable=True))
    op.execute("UPDATE projects SET type = 'consulting' WHERE type IS NULL")
    op.alter_column("projects", "type", nullable=False)
    op.drop_column("projects", "status")


def downgrade() -> None:
    op.add_column("projects", sa.Column("status", sa.String(20), nullable=True))
    op.execute("UPDATE projects SET status = 'in_progress' WHERE status IS NULL")
    op.alter_column("projects", "status", nullable=False)
    op.drop_column("projects", "type")
