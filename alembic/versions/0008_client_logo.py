"""client logo

Revision ID: 0008
Revises: 0007
Create Date: 2026-07-20

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0008"
down_revision: str | None = "0007"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("clients", sa.Column("logo_file_id", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("clients", "logo_file_id")
