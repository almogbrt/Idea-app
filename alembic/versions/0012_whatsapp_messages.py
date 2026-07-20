"""whatsapp messages

Revision ID: 0012
Revises: 0011
Create Date: 2026-07-20

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012"
down_revision: str | None = "0011"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "whatsapp_messages",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column(
            "user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        ),
        sa.Column("phone_number", sa.String(32), nullable=False),
        sa.Column("sequence", sa.BigInteger(), sa.Identity(), nullable=False, unique=True),
        sa.Column("direction", sa.String(10), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_whatsapp_messages_user_id", "whatsapp_messages", ["user_id"])
    op.create_index(
        "ix_whatsapp_messages_phone_sequence", "whatsapp_messages", ["phone_number", "sequence"]
    )


def downgrade() -> None:
    op.drop_index("ix_whatsapp_messages_phone_sequence", table_name="whatsapp_messages")
    op.drop_index("ix_whatsapp_messages_user_id", table_name="whatsapp_messages")
    op.drop_table("whatsapp_messages")
