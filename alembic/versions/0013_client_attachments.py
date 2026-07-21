"""client attachments

Revision ID: 0013
Revises: 0012
Create Date: 2026-07-21

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0013"
down_revision: str | None = "0012"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "client_attachments",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column(
            "client_id",
            sa.Uuid(),
            sa.ForeignKey("clients.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("file_id", sa.String(255), nullable=False),
        sa.Column("filename", sa.String(500), nullable=False),
        sa.Column("mime_type", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index(
        "ix_client_attachments_client_id", "client_attachments", ["client_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_client_attachments_client_id", table_name="client_attachments")
    op.drop_table("client_attachments")
