from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.conversation_repository import ConversationRepositoryPort
from app.domain.entities import Conversation, Message, MessageRole, ToolCall
from app.infrastructure.db.models import ConversationModel, MessageModel


class SqlAlchemyConversationRepository(ConversationRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_conversation(self, user_id: uuid.UUID, title: str) -> Conversation:
        row = ConversationModel(user_id=user_id, title=title)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._conversation_to_entity(row)

    async def get_conversation(self, conversation_id: uuid.UUID) -> Conversation | None:
        row = await self._session.get(ConversationModel, conversation_id)
        return self._conversation_to_entity(row) if row else None

    async def get_or_create_by_title(self, user_id: uuid.UUID, title: str) -> Conversation:
        stmt = select(ConversationModel).where(
            ConversationModel.user_id == user_id, ConversationModel.title == title
        )
        row = (await self._session.scalars(stmt)).first()
        if row is not None:
            return self._conversation_to_entity(row)
        return await self.create_conversation(user_id, title)

    async def append_message(self, message: Message) -> Message:
        row = MessageModel(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role.value,
            content=message.content,
            tool_calls=[
                {"id": tc.id, "tool_name": tc.tool_name, "arguments": tc.arguments}
                for tc in message.tool_calls
            ],
            tool_call_id=message.tool_call_id,
        )
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._message_to_entity(row)

    async def get_recent_messages(
        self, conversation_id: uuid.UUID, limit: int = 20
    ) -> list[Message]:
        stmt = (
            select(MessageModel)
            .where(MessageModel.conversation_id == conversation_id)
            .order_by(MessageModel.sequence.desc())
            .limit(limit)
        )
        rows = (await self._session.scalars(stmt)).all()
        return [self._message_to_entity(row) for row in reversed(rows)]

    @staticmethod
    def _conversation_to_entity(row: ConversationModel) -> Conversation:
        return Conversation(
            id=row.id, user_id=row.user_id, title=row.title, created_at=row.created_at
        )

    @staticmethod
    def _message_to_entity(row: MessageModel) -> Message:
        return Message(
            id=row.id,
            conversation_id=row.conversation_id,
            role=MessageRole(row.role),
            content=row.content,
            created_at=row.created_at,
            tool_calls=[
                ToolCall(id=tc["id"], tool_name=tc["tool_name"], arguments=tc["arguments"])
                for tc in row.tool_calls
            ],
            tool_call_id=row.tool_call_id,
        )
