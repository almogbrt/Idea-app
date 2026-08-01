"""task urgency

Revision ID: 0019
Revises: 0018
Create Date: 2026-07-27

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0019"
down_revision: str | None = "0018"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("urgency", sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column("tasks", "urgency")
