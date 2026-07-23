from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.application.ports.calendar_port import CalendarPort
from app.application.ports.drive_port import DrivePort
from app.application.ports.email_sender import EmailSenderPort
from app.application.ports.inbox import InboxPort
from app.application.ports.schedule import SchedulePort
from app.application.use_cases.check_reminders import CheckRemindersUseCase
from app.application.use_cases.manage_calendar import ManageCalendarUseCase
from app.application.use_cases.manage_daily_plan import (
    DailyPlanMetricsUseCase,
    ManageDailyPlanUseCase,
    ManageFocusSessionUseCase,
    ManageGoalsUseCase,
)
from app.application.use_cases.manage_email import ManageEmailUseCase
from app.application.use_cases.manage_files import ManageFilesUseCase
from app.application.use_cases.manage_notifications import ManageNotificationsUseCase
from app.application.use_cases.manage_whatsapp_messages import ManageWhatsAppMessagesUseCase
from app.application.use_cases.manage_workspace import (
    DashboardSummaryUseCase,
    ListActivityUseCase,
    ManageClientsUseCase,
    ManageProjectsUseCase,
    ManageTasksUseCase,
    ManageThoughtsUseCase,
)
from app.application.use_cases.send_daily_review import SendDailyReviewUseCase
from app.core.container import RequestScopedServices
from app.domain.entities import (
    CalendarEvent,
    Conversation,
    DriveFile,
    EmailSummary,
    OrchestrationResult,
    ToolCall,
    User,
)
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from tests.conftest import (
    FakeAgentExecutionRepository,
    FakeClientAttachmentRepository,
    FakeClientLogoStorage,
    FakeClientRepository,
    FakeDailyPlanRepository,
    FakeDailyPlanSwapRepository,
    FakeFocusSessionRepository,
    FakeGoalRepository,
    FakeNotificationRepository,
    FakeProjectRepository,
    FakeTaskRepository,
    FakeThoughtRepository,
    FakeUserRepository,
    FakeWhatsAppMessageRepository,
)


class _NullInbox(InboxPort):
    async def count_unread(self, user_id: uuid.UUID) -> int:
        return 0

    async def list_recent(self, user_id: uuid.UUID, max_results: int) -> list[EmailSummary]:
        return []


class _NullSchedule(SchedulePort):
    async def count_meetings_today(self, user_id: uuid.UUID) -> int:
        return 0


class _NullEmailSender(EmailSenderPort):
    async def send(self, user_id: uuid.UUID, to: str, subject: str, body: str) -> None:
        return None


class _NullCalendar(CalendarPort):
    async def list_between(
        self, user_id: uuid.UUID, time_min: str, time_max: str
    ) -> list[CalendarEvent]:
        return []

    async def create(
        self,
        user_id: uuid.UUID,
        summary: str,
        start_time: str,
        end_time: str,
        description: str | None = None,
    ) -> CalendarEvent:
        raise NotImplementedError

    async def delete(self, user_id: uuid.UUID, event_id: str) -> None:
        raise NotImplementedError


class _NullDrive(DrivePort):
    async def list_files(
        self,
        user_id: uuid.UUID,
        query: str | None,
        max_results: int,
        order_by: str | None = None,
    ) -> list[DriveFile]:
        return []

    async def get_content(self, user_id: uuid.UUID, file_id: str) -> str:
        raise NotImplementedError

    async def create_file(
        self, user_id: uuid.UUID, name: str, content: str, mime_type: str
    ) -> DriveFile:
        raise NotImplementedError

    async def share_file(self, user_id: uuid.UUID, file_id: str, email: str, role: str) -> None:
        raise NotImplementedError


def _workspace_kwargs() -> dict[str, object]:
    clients_repo = FakeClientRepository()
    projects_repo = FakeProjectRepository(clients_repo)
    tasks_repo = FakeTaskRepository()
    notifications_repo = FakeNotificationRepository()
    inbox_port = _NullInbox()
    return {
        "manage_clients": ManageClientsUseCase(
            clients_repo,
            projects_repo,
            tasks_repo,
            FakeClientLogoStorage(),
            FakeClientAttachmentRepository(),
        ),
        "manage_projects": ManageProjectsUseCase(projects_repo),
        "manage_tasks": ManageTasksUseCase(tasks_repo),
        "manage_thoughts": ManageThoughtsUseCase(FakeThoughtRepository()),
        "manage_whatsapp_messages": ManageWhatsAppMessagesUseCase(FakeWhatsAppMessageRepository()),
        "dashboard_summary": DashboardSummaryUseCase(
            projects_repo, tasks_repo, clients_repo, inbox_port, _NullSchedule()
        ),
        "list_activity": ListActivityUseCase(FakeAgentExecutionRepository()),
        "manage_notifications": ManageNotificationsUseCase(notifications_repo),
        "check_reminders": CheckRemindersUseCase(
            FakeUserRepository(),
            tasks_repo,
            notifications_repo,
            _NullEmailSender(),
            _NullCalendar(),
        ),
        "send_daily_review": SendDailyReviewUseCase(
            FakeUserRepository(),
            tasks_repo,
            _NullCalendar(),
            notifications_repo,
            _NullEmailSender(),
            FakeDailyPlanRepository(),
        ),
        "manage_calendar": ManageCalendarUseCase(_NullCalendar()),
        "manage_email": ManageEmailUseCase(inbox_port),
        "manage_files": ManageFilesUseCase(_NullDrive()),
        "manage_goals": ManageGoalsUseCase(FakeGoalRepository()),
        "manage_daily_plan": ManageDailyPlanUseCase(
            FakeDailyPlanRepository(), FakeDailyPlanSwapRepository(), tasks_repo
        ),
        "manage_focus_sessions": ManageFocusSessionUseCase(
            FakeFocusSessionRepository(), FakeDailyPlanRepository()
        ),
        "daily_plan_metrics": DailyPlanMetricsUseCase(
            FakeDailyPlanRepository(),
            FakeFocusSessionRepository(),
            FakeDailyPlanSwapRepository(),
            tasks_repo,
        ),
        "finance_overview": None,
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
