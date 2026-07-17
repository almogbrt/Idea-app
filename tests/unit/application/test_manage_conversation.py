from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from app.application.use_cases.manage_conversation import ManageConversationUseCase
from app.core.exceptions import NotFoundError
from app.domain.entities import Message, MessageRole
from tests.conftest import FakeConversationRepository


async def test_start_conversation_creates_and_persists(
    fake_conversation_repository: FakeConversationRepository,
) -> None:
    use_case = ManageConversationUseCase(fake_conversation_repository)
    user_id = uuid.uuid4()

    conversation = await use_case.start_conversation(user_id, title="My first chat")

    assert conversation.user_id == user_id
    assert conversation.title == "My first chat"
    assert conversation.id in fake_conversation_repository.conversations


async def test_get_conversation_or_raise_raises_when_missing(
    fake_conversation_repository: FakeConversationRepository,
) -> None:
    use_case = ManageConversationUseCase(fake_conversation_repository)
    with pytest.raises(NotFoundError):
        await use_case.get_conversation_or_raise(uuid.uuid4())


async def test_get_history_returns_recent_messages_in_order(
    fake_conversation_repository: FakeConversationRepository,
) -> None:
    use_case = ManageConversationUseCase(fake_conversation_repository)
    user_id = uuid.uuid4()
    conversation = await use_case.start_conversation(user_id)

    for i in range(3):
        await fake_conversation_repository.append_message(
            Message(
                id=uuid.uuid4(),
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content=f"message {i}",
                created_at=datetime.now(UTC),
            )
        )

    history = await use_case.get_history(conversation.id, limit=2)
    assert [m.content for m in history] == ["message 1", "message 2"]
