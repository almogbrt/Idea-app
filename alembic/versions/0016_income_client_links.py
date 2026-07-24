"""income client links

Revision ID: 0016
Revises: 0015
Create Date: 2026-07-24

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0016"
down_revision: str | None = "0015"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "income_client_links",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("green_invoice_client_id", sa.String(255), nullable=False),
        sa.Column("green_invoice_client_name", sa.String(500), nullable=False),
        sa.Column(
            "client_id",
            sa.Uuid(),
            sa.ForeignKey("clients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_unique_constraint(
        "uq_income_client_links_user_gi_client",
        "income_client_links",
        ["user_id", "green_invoice_client_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_income_client_links_user_gi_client", "income_client_links", type_="unique"
    )
    op.drop_table("income_client_links")
