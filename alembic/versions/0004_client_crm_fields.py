"""client crm fields

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-18

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("clients", sa.Column("email", sa.String(320), nullable=True))
    op.add_column("clients", sa.Column("phone", sa.String(50), nullable=True))
    op.add_column("clients", sa.Column("notes", sa.Text(), nullable=True))
    op.add_column(
        "clients", sa.Column("next_follow_up_at", sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("clients", "next_follow_up_at")
    op.drop_column("clients", "notes")
    op.drop_column("clients", "phone")
    op.drop_column("clients", "email")
