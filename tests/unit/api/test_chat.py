from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.application.ports.inbox import InboxPort
from app.application.ports.schedule import SchedulePort
from app.application.use_cases.manage_workspace import (
    DashboardSummaryUseCase,
    ListActivityUseCase,
    ManageClientsUseCase,
    ManageProjectsUseCase,
    ManageTasksUseCase,
)
from app.core.container import RequestScopedServices
from app.domain.entities import Conversation, OrchestrationResult, ToolCall, User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from tests.conftest import (
    FakeAgentExecutionRepository,
    FakeClientRepository,
    FakeProjectRepository,
    FakeTaskRepository,
)


class _NullInbox(InboxPort):
    async def count_unread(self, user_id: uuid.UUID) -> int:
        return 0


class _NullSchedule(SchedulePort):
    async def count_meetings_today(self, user_id: uuid.UUID) -> int:
        return 0


def _workspace_kwargs() -> dict[str, object]:
    projects_repo = FakeProjectRepository()
    tasks_repo = FakeTaskRepository()
    return {
        "manage_clients": ManageClientsUseCase(FakeClientRepository()),
        "manage_projects": ManageProjectsUseCase(projects_repo),
        "manage_tasks": ManageTasksUseCase(tasks_repo),
        "dashboard_summary": DashboardSummaryUseCase(
            projects_repo, tasks_repo, _NullInbox(), _NullSchedule()
        ),
        "list_activity": ListActivityUseCase(FakeAgentExecutionRepository()),
    }

_USER = User(
    id=uuid.uuid4(),
    google_sub="sub-1",
    email="owner@example.com",
    name="Owner",
    created_at=datetime.now(UTC),
)


@dataclass
class _FakeOrchestrator:
    reply: str
    tool_calls: list[ToolCall]

    async def handle_command(
        self, *, user_id: uuid.UUID, conversation_id: uuid.UUID, text: str
    ) -> OrchestrationResult:
        return OrchestrationResult(
            reply=self.reply, conversation_id=conversation_id, tool_calls_made=self.tool_calls
        )


class _FakeManageConversation:
    def __init__(self, owner_id: uuid.UUID) -> None:
        self._owner_id = owner_id
        self.conversation = Conversation(
            id=uuid.uuid4(), user_id=owner_id, title="test", created_at=datetime.now(UTC)
        )

    async def start_conversation(
        self, user_id: uuid.UUID, title: str = "New conversation"
    ) -> Conversation:
        return self.conversation

    async def get_conversation_or_raise(self, conversation_id: uuid.UUID) -> Conversation:
        return self.conversation

    async def get_history(self, conversation_id: uuid.UUID, limit: int = 20) -> list:
        return []


def _override_scope(
    client: TestClient, reply: str, tool_calls: list[ToolCall] | None = None
) -> None:
    manage_conversation = _FakeManageConversation(_USER.id)
    scope = RequestScopedServices(
        orchestrator=_FakeOrchestrator(reply=reply, tool_calls=tool_calls or []),  # type: ignore[arg-type]
        manage_conversation=manage_conversation,  # type: ignore[arg-type]
        authenticate_user=None,  # type: ignore[arg-type]
        **_workspace_kwargs(),  # type: ignore[arg-type]
    )
    client.app.dependency_overrides[get_current_user] = lambda: _USER
    client.app.dependency_overrides[get_request_scope] = lambda: scope


def test_send_command_creates_conversation_and_returns_reply(client: TestClient) -> None:
    _override_scope(client, reply="Done! I created the file.")

    response = client.post("/api/v1/chat/commands", json={"text": "create a file called notes.txt"})

    assert response.status_code == 200
    body = response.json()
    assert body["reply"] == "Done! I created the file."
    assert "conversation_id" in body


def test_send_command_requires_authentication(client: TestClient) -> None:
    response = client.post("/api/v1/chat/commands", json={"text": "hello"})
    assert response.status_code == 401


def test_get_conversation_history_rejects_other_users_conversation(client: TestClient) -> None:
    _override_scope(client, reply="ok")
    other_conversation_id = uuid.uuid4()

    # the fake ManageConversation always returns a conversation owned by _USER, so to
    # exercise the ownership check we point at a conversation belonging to someone else.
    class _OtherOwnerConversation(_FakeManageConversation):
        async def get_conversation_or_raise(self, conversation_id: uuid.UUID) -> Conversation:
            return Conversation(
                id=conversation_id,
                user_id=uuid.uuid4(),
                title="not yours",
                created_at=datetime.now(UTC),
            )

    scope = RequestScopedServices(
        orchestrator=_FakeOrchestrator(reply="ok", tool_calls=[]),  # type: ignore[arg-type]
        manage_conversation=_OtherOwnerConversation(_USER.id),  # type: ignore[arg-type]
        authenticate_user=None,  # type: ignore[arg-type]
        **_workspace_kwargs(),  # type: ignore[arg-type]
    )
    client.app.dependency_overrides[get_current_user] = lambda: _USER
    client.app.dependency_overrides[get_request_scope] = lambda: scope

    response = client.get(f"/api/v1/chat/conversations/{other_conversation_id}")
    assert response.status_code == 403
