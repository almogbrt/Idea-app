"""message tool_call_id

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-19

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("messages", sa.Column("tool_call_id", sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column("messages", "tool_call_id")
