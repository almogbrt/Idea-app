from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SendCommandRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=8000)
    conversation_id: uuid.UUID | None = None


class ToolCallView(BaseModel):
    id: str
    tool_name: str
    arguments: dict[str, Any]


class SendCommandResponse(BaseModel):
    reply: str
    conversation_id: uuid.UUID
    tool_calls_made: list[ToolCallView]


class MessageView(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    created_at: datetime


class ConversationView(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime


class ConversationHistoryResponse(BaseModel):
    conversation: ConversationView
    messages: list[MessageView]
