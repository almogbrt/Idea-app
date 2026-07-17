"""The primary entry point into Edith: natural-language commands in, routed
tool execution + a natural-language reply out."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends

from app.core.container import RequestScopedServices
from app.core.exceptions import ForbiddenError
from app.domain.entities import Conversation, User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from app.interfaces.api.schemas.chat import (
    ConversationHistoryResponse,
    ConversationView,
    MessageView,
    SendCommandRequest,
    SendCommandResponse,
    ToolCallView,
)

router = APIRouter(prefix="/chat", tags=["chat"])


def _ensure_owned_by(conversation: Conversation, user: User) -> None:
    if conversation.user_id != user.id:
        raise ForbiddenError("This conversation does not belong to you.")


@router.post("/commands", response_model=SendCommandResponse)
async def send_command(
    body: SendCommandRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> SendCommandResponse:
    conversation_id = body.conversation_id
    if conversation_id is None:
        conversation = await scope.manage_conversation.start_conversation(user.id)
        conversation_id = conversation.id
    else:
        conversation = await scope.manage_conversation.get_conversation_or_raise(conversation_id)
        _ensure_owned_by(conversation, user)

    result = await scope.orchestrator.handle_command(
        user_id=user.id, conversation_id=conversation_id, text=body.text
    )

    return SendCommandResponse(
        reply=result.reply,
        conversation_id=result.conversation_id,
        tool_calls_made=[
            ToolCallView(id=tc.id, tool_name=tc.tool_name, arguments=tc.arguments)
            for tc in result.tool_calls_made
        ],
    )


@router.get("/conversations/{conversation_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    conversation_id: str,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> ConversationHistoryResponse:
    conversation = await scope.manage_conversation.get_conversation_or_raise(
        uuid.UUID(conversation_id)
    )
    _ensure_owned_by(conversation, user)
    messages = await scope.manage_conversation.get_history(conversation.id)

    return ConversationHistoryResponse(
        conversation=ConversationView(
            id=conversation.id, title=conversation.title, created_at=conversation.created_at
        ),
        messages=[
            MessageView(id=m.id, role=m.role.value, content=m.content, created_at=m.created_at)
            for m in messages
        ],
    )
