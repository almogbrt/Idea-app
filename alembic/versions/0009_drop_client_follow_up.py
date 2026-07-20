"""drop client follow-up

Revision ID: 0009
Revises: 0008
Create Date: 2026-07-20

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009"
down_revision: str | None = "0008"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("clients", "next_follow_up_at")


def downgrade() -> None:
    op.add_column(
        "clients", sa.Column("next_follow_up_at", sa.DateTime(timezone=True), nullable=True)
    )
