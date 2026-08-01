"""SQLAlchemy ORM models — the only place the Postgres schema is defined.

Domain entities (`app/domain/entities.py`) stay framework-free; repository
adapters in this package translate between these ORM rows and domain
dataclasses at the boundary.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

EMBEDDING_DIMENSIONS = 1536

_TIMESTAMPTZ = DateTime(timezone=True)


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    google_sub: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())


class OAuthTokenModel(Base):
    __tablename__ = "oauth_tokens"
    __table_args__ = (Index("ix_oauth_tokens_user_provider", "user_id", "provider", unique=True),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    provider: Mapped[str] = mapped_column(String(50))
    access_token_enc: Mapped[str] = mapped_column(String)
    refresh_token_enc: Mapped[str | None] = mapped_column(String, nullable=True)
    scopes: Mapped[list[str]] = mapped_column(JSONB, default=list)
    expiry: Mapped[datetime] = mapped_column(_TIMESTAMPTZ)
    updated_at: Mapped[datetime] = mapped_column(
        _TIMESTAMPTZ, server_default=func.now(), onupdate=func.now()
    )


class ConversationModel(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())

    messages: Mapped[list[MessageModel]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="MessageModel.sequence",
    )


class MessageModel(Base):
    """`sequence` (not `created_at`) is the ordering key: Postgres's `now()` is
    frozen for the duration of a transaction, so several messages persisted in
    the same transaction can share an identical `created_at` — a monotonic
    identity column is the only reliable way to preserve insertion order."""

    __tablename__ = "messages"
    __table_args__ = (Index("ix_messages_conversation_sequence", "conversation_id", "sequence"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE")
    )
    sequence: Mapped[int] = mapped_column(BigInteger, Identity(), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column()
    tool_calls: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, default=list)
    tool_call_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())

    conversation: Mapped[ConversationModel] = relationship(back_populates="messages")


class MemoryRecordModel(Base):
    __tablename__ = "memory_records"
    __table_args__ = (Index("ix_memory_records_user_id", "user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column()
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIMENSIONS))
    record_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())


class AgentExecutionModel(Base):
    __tablename__ = "agent_executions"
    __table_args__ = (Index("ix_agent_executions_user_created", "user_id", "created_at"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    agent_name: Mapped[str] = mapped_column(String(100))
    tool_name: Mapped[str] = mapped_column(String(150))
    input: Mapped[dict[str, Any]] = mapped_column(JSONB)
    output: Mapped[dict[str, Any]] = mapped_column(JSONB)
    status: Mapped[str] = mapped_column(String(20))
    latency_ms: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())


class ClientModel(Base):
    __tablename__ = "clients"
    __table_args__ = (Index("ix_clients_user_id", "user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(nullable=True)
    logo_file_id: Mapped[str | None] = mapped_column(String(255), nullable=True)


class ClientAttachmentModel(Base):
    __tablename__ = "client_attachments"
    __table_args__ = (Index("ix_client_attachments_client_id", "client_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))
    file_id: Mapped[str] = mapped_column(String(255))
    filename: Mapped[str] = mapped_column(String(500))
    mime_type: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())


class IncomeClientLinkModel(Base):
    __tablename__ = "income_client_links"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "green_invoice_client_id", name="uq_income_client_links_user_gi_client"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    green_invoice_client_id: Mapped[str] = mapped_column(String(255))
    green_invoice_client_name: Mapped[str] = mapped_column(String(500))
    client_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())


class ProjectModel(Base):
    __tablename__ = "projects"
    __table_args__ = (Index("ix_projects_user_id", "user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    client_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        _TIMESTAMPTZ, server_default=func.now(), onupdate=func.now()
    )


class TaskModel(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        Index("ix_tasks_user_id", "user_id"),
        Index("ix_tasks_project_id", "project_id"),
        Index("ix_tasks_client_id", "client_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        _TIMESTAMPTZ, server_default=func.now(), onupdate=func.now()
    )
    due_at: Mapped[datetime | None] = mapped_column(_TIMESTAMPTZ, nullable=True)
    client_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )
    start_at: Mapped[datetime | None] = mapped_column(_TIMESTAMPTZ, nullable=True)
    timer_started_at: Mapped[datetime | None] = mapped_column(_TIMESTAMPTZ, nullable=True)
    deliverable: Mapped[str | None] = mapped_column(nullable=True)
    estimated_minutes: Mapped[int | None] = mapped_column(nullable=True)
    importance: Mapped[str | None] = mapped_column(String(20), nullable=True)
    goal_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("goals.id", ondelete="SET NULL"), nullable=True
    )
    next_step: Mapped[str | None] = mapped_column(nullable=True)
    category: Mapped[str | None] = mapped_column(String(20), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(_TIMESTAMPTZ, nullable=True)
    urgency: Mapped[str | None] = mapped_column(String(20), nullable=True)


class ThoughtModel(Base):
    __tablename__ = "thoughts"
    __table_args__ = (Index("ix_thoughts_user_id", "user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())


class WhatsAppMessageModel(Base):
    """`sequence` (not `created_at`) is the ordering key — see `MessageModel`
    above: Postgres's `now()` is frozen for the duration of a transaction, so
    several messages logged in the same transaction (e.g. a webhook batch)
    can share an identical `created_at`."""

    __tablename__ = "whatsapp_messages"
    __table_args__ = (
        Index("ix_whatsapp_messages_user_id", "user_id"),
        Index("ix_whatsapp_messages_phone_sequence", "phone_number", "sequence"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    phone_number: Mapped[str] = mapped_column(String(32))
    sequence: Mapped[int] = mapped_column(BigInteger, Identity(), unique=True, nullable=False)
    direction: Mapped[str] = mapped_column(String(10))
    content: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())


class NotificationModel(Base):
    __tablename__ = "notifications"
    __table_args__ = (
        Index("ix_notifications_user_id", "user_id"),
        Index("ix_notifications_kind_related_id", "kind", "related_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    kind: Mapped[str] = mapped_column(String(50))
    related_id: Mapped[uuid.UUID] = mapped_column()
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())
    read_at: Mapped[datetime | None] = mapped_column(_TIMESTAMPTZ, nullable=True)


class GoalModel(Base):
    __tablename__ = "goals"
    __table_args__ = (Index("ix_goals_user_id", "user_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())


class DailyPlanModel(Base):
    __tablename__ = "daily_plans"
    __table_args__ = (
        Index("ix_daily_plans_user_id", "user_id"),
        UniqueConstraint("user_id", "plan_date", name="uq_daily_plans_user_id_plan_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    plan_date: Mapped[date] = mapped_column(Date)
    main_task_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    secondary_task_id_1: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    secondary_task_id_2: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    is_locked: Mapped[bool] = mapped_column(Boolean, server_default="false")
    locked_at: Mapped[datetime | None] = mapped_column(_TIMESTAMPTZ, nullable=True)
    carry_over_task_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        _TIMESTAMPTZ, server_default=func.now(), onupdate=func.now()
    )


class FocusSessionModel(Base):
    __tablename__ = "focus_sessions"
    __table_args__ = (
        Index("ix_focus_sessions_user_id", "user_id"),
        Index("ix_focus_sessions_daily_plan_id", "daily_plan_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    daily_plan_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("daily_plans.id", ondelete="CASCADE")
    )
    started_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())
    ended_at: Mapped[datetime | None] = mapped_column(_TIMESTAMPTZ, nullable=True)
    exit_reason: Mapped[str | None] = mapped_column(String(20), nullable=True)
    stuck_reason: Mapped[str | None] = mapped_column(String(20), nullable=True)


class DailyPlanSwapModel(Base):
    __tablename__ = "daily_plan_swaps"
    __table_args__ = (Index("ix_daily_plan_swaps_daily_plan_id", "daily_plan_id"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    daily_plan_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("daily_plans.id", ondelete="CASCADE")
    )
    bumped_task_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    new_task_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(_TIMESTAMPTZ, server_default=func.now())
