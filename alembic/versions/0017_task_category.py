"""task category

Revision ID: 0017
Revises: 0016
Create Date: 2026-07-26

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0017"
down_revision: str | None = "0016"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("tasks", sa.Column("category", sa.String(20), nullable=True))


def downgrade() -> None:
    op.drop_column("tasks", "category")
