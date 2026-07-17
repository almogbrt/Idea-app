"""Shared test doubles for the ports defined in `app/application/ports/`.

These are plain in-memory implementations, not mocks — they let unit tests
exercise real use case / orchestrator logic without touching Postgres,
Redis, Anthropic, or Google.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import pytest

from app.application.ports.agent_execution_repository import AgentExecutionRepositoryPort
from app.application.ports.conversation_repository import ConversationRepositoryPort
from app.application.ports.embedding import EmbeddingPort
from app.application.ports.llm_gateway import LLMGatewayPort, LLMMessage, LLMResponse, LLMStopReason
from app.application.ports.memory_repository import MemoryRepositoryPort
from app.application.ports.oauth_token_repository import OAuthTokenRepositoryPort
from app.application.ports.user_repository import UserRepositoryPort
from app.domain.entities import (
    AgentExecution,
    Conversation,
    MemoryRecord,
    Message,
    ToolDefinition,
    User,
)
from app.domain.value_objects import OAuthTokenSet


class FakeConversationRepository(ConversationRepositoryPort):
    def __init__(self) -> None:
        self.conversations: dict[uuid.UUID, Conversation] = {}
        self.messages: dict[uuid.UUID, list[Message]] = {}

    async def create_conversation(self, user_id: uuid.UUID, title: str) -> Conversation:
        conversation = Conversation(
            id=uuid.uuid4(), user_id=user_id, title=title, created_at=datetime.now(UTC)
        )
        self.conversations[conversation.id] = conversation
        self.messages[conversation.id] = []
        return conversation

    async def get_conversation(self, conversation_id: uuid.UUID) -> Conversation | None:
        return self.conversations.get(conversation_id)

    async def append_message(self, message: Message) -> Message:
        self.messages.setdefault(message.conversation_id, []).append(message)
        return message

    async def get_recent_messages(
        self, conversation_id: uuid.UUID, limit: int = 20
    ) -> list[Message]:
        return self.messages.get(conversation_id, [])[-limit:]


class FakeMemoryRepository(MemoryRepositoryPort):
    def __init__(self) -> None:
        self.records: list[MemoryRecord] = []

    async def store(
        self,
        user_id: uuid.UUID,
        content: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> MemoryRecord:
        record = MemoryRecord(
            id=uuid.uuid4(),
            user_id=user_id,
            content=content,
            metadata=metadata or {},
            created_at=datetime.now(UTC),
            embedding=embedding,
        )
        self.records.append(record)
        return record

    async def search(
        self, user_id: uuid.UUID, query_embedding: list[float], top_k: int = 5
    ) -> list[MemoryRecord]:
        return [r for r in self.records if r.user_id == user_id][:top_k]


class FakeAgentExecutionRepository(AgentExecutionRepositoryPort):
    def __init__(self) -> None:
        self.executions: list[AgentExecution] = []

    async def record(self, execution: AgentExecution) -> None:
        self.executions.append(execution)


class FakeOAuthTokenRepository(OAuthTokenRepositoryPort):
    def __init__(self) -> None:
        self.tokens: dict[tuple[uuid.UUID, str], OAuthTokenSet] = {}

    async def save_tokens(self, user_id: uuid.UUID, provider: str, tokens: OAuthTokenSet) -> None:
        self.tokens[(user_id, provider)] = tokens

    async def get_tokens(self, user_id: uuid.UUID, provider: str) -> OAuthTokenSet | None:
        return self.tokens.get((user_id, provider))


class FakeUserRepository(UserRepositoryPort):
    def __init__(self) -> None:
        self.users: dict[uuid.UUID, User] = {}

    async def get_by_google_sub(self, google_sub: str) -> User | None:
        return next((u for u in self.users.values() if u.google_sub == google_sub), None)

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.users.get(user_id)

    async def create(self, google_sub: str, email: str, name: str) -> User:
        user = User(
            id=uuid.uuid4(),
            google_sub=google_sub,
            email=email,
            name=name,
            created_at=datetime.now(UTC),
        )
        self.users[user.id] = user
        return user


class FakeEmbeddingGateway(EmbeddingPort):
    """Deterministic fake: embeds text as a hash-derived vector."""

    async def embed(self, text: str) -> list[float]:
        return [float((hash(text) >> (i * 4)) % 10) for i in range(8)]


@dataclass
class ScriptedLLMGateway(LLMGatewayPort):
    """Replays a fixed sequence of responses, one per call to `generate`."""

    responses: list[LLMResponse]
    calls: list[dict[str, Any]] = field(default_factory=list)

    async def generate(
        self, *, system_prompt: str, messages: list[LLMMessage], tools: list[ToolDefinition]
    ) -> LLMResponse:
        self.calls.append({"system_prompt": system_prompt, "messages": messages, "tools": tools})
        index = len(self.calls) - 1
        if index >= len(self.responses):
            return LLMResponse(
                content="(no more scripted responses)",
                tool_calls=(),
                stop_reason=LLMStopReason.END_TURN,
            )
        return self.responses[index]


@pytest.fixture
def fake_conversation_repository() -> FakeConversationRepository:
    return FakeConversationRepository()


@pytest.fixture
def fake_memory_repository() -> FakeMemoryRepository:
    return FakeMemoryRepository()


@pytest.fixture
def fake_agent_execution_repository() -> FakeAgentExecutionRepository:
    return FakeAgentExecutionRepository()


@pytest.fixture
def fake_oauth_token_repository() -> FakeOAuthTokenRepository:
    return FakeOAuthTokenRepository()


@pytest.fixture
def fake_user_repository() -> FakeUserRepository:
    return FakeUserRepository()


@pytest.fixture
def fake_embedding_gateway() -> FakeEmbeddingGateway:
    return FakeEmbeddingGateway()
