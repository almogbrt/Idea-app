from __future__ import annotations

import uuid

from app.application.ports.conversation_repository import ConversationRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import Conversation, Message


class ManageConversationUseCase:
    def __init__(self, conversation_repository: ConversationRepositoryPort) -> None:
        self._conversations = conversation_repository

    async def start_conversation(
        self, user_id: uuid.UUID, title: str = "New conversation"
    ) -> Conversation:
        return await self._conversations.create_conversation(user_id, title)

    async def get_or_create_by_title(self, user_id: uuid.UUID, title: str) -> Conversation:
        return await self._conversations.get_or_create_by_title(user_id, title)

    async def get_conversation_or_raise(self, conversation_id: uuid.UUID) -> Conversation:
        conversation = await self._conversations.get_conversation(conversation_id)
        if conversation is None:
            raise NotFoundError(
                "Conversation not found", details={"conversation_id": str(conversation_id)}
            )
        return conversation

    async def get_history(self, conversation_id: uuid.UUID, limit: int = 20) -> list[Message]:
        return await self._conversations.get_recent_messages(conversation_id, limit=limit)
