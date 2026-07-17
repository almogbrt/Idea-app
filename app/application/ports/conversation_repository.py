from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import Conversation, Message


class ConversationRepositoryPort(ABC):
    @abstractmethod
    async def create_conversation(self, user_id: uuid.UUID, title: str) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    async def get_conversation(self, conversation_id: uuid.UUID) -> Conversation | None:
        raise NotImplementedError

    @abstractmethod
    async def append_message(self, message: Message) -> Message:
        raise NotImplementedError

    @abstractmethod
    async def get_recent_messages(
        self, conversation_id: uuid.UUID, limit: int = 20
    ) -> list[Message]:
        """Returns messages ordered oldest-first, most recent `limit` only."""
        raise NotImplementedError
