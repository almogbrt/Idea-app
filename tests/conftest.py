"""Shared test doubles for the ports defined in `app/application/ports/`.

These are plain in-memory implementations, not mocks — they let unit tests
exercise real use case / orchestrator logic without touching Postgres,
Redis, Anthropic, or Google.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from typing import Any

import pytest

from app.application.ports.agent_execution_repository import AgentExecutionRepositoryPort
from app.application.ports.cache import CachePort
from app.application.ports.calendar_port import CalendarPort
from app.application.ports.client_attachment_repository import ClientAttachmentRepositoryPort
from app.application.ports.client_logo_storage import ClientLogoStoragePort
from app.application.ports.client_repository import ClientRepositoryPort
from app.application.ports.conversation_repository import ConversationRepositoryPort
from app.application.ports.daily_plan_repository import DailyPlanRepositoryPort
from app.application.ports.daily_plan_swap_repository import DailyPlanSwapRepositoryPort
from app.application.ports.embedding import EmbeddingPort
from app.application.ports.focus_session_repository import FocusSessionRepositoryPort
from app.application.ports.goal_repository import GoalRepositoryPort
from app.application.ports.green_invoice_port import GreenInvoicePort
from app.application.ports.llm_gateway import LLMGatewayPort, LLMMessage, LLMResponse, LLMStopReason
from app.application.ports.memory_repository import MemoryRepositoryPort
from app.application.ports.notification_repository import NotificationRepositoryPort
from app.application.ports.oauth_token_repository import OAuthTokenRepositoryPort
from app.application.ports.project_repository import ProjectRepositoryPort
from app.application.ports.task_repository import TaskRepositoryPort
from app.application.ports.thought_repository import ThoughtRepositoryPort
from app.application.ports.user_repository import UserRepositoryPort
from app.application.ports.whatsapp_message_repository import WhatsAppMessageRepositoryPort
from app.core.exceptions import AppError, NotFoundError
from app.domain.entities import (
    AgentExecution,
    CalendarEvent,
    Client,
    ClientAttachment,
    Conversation,
    DailyPlan,
    DailyPlanSwap,
    ExpenseRecord,
    FocusExitReason,
    FocusSession,
    FocusStuckReason,
    Goal,
    IncomeRecord,
    MemoryRecord,
    Message,
    Notification,
    NotificationKind,
    Project,
    ProjectSummary,
    ProjectType,
    Task,
    TaskImportance,
    TaskStatus,
    Thought,
    ToolDefinition,
    User,
    WhatsAppDirection,
    WhatsAppMessage,
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

    async def get_or_create_by_title(self, user_id: uuid.UUID, title: str) -> Conversation:
        existing = next(
            (
                c
                for c in self.conversations.values()
                if c.user_id == user_id and c.title == title
            ),
            None,
        )
        if existing is not None:
            return existing
        return await self.create_conversation(user_id, title)

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

    async def list_recent(self, user_id: uuid.UUID, limit: int = 10) -> list[AgentExecution]:
        matching = [e for e in self.executions if e.user_id == user_id]
        return list(reversed(matching))[:limit]


class FakeClientRepository(ClientRepositoryPort):
    def __init__(self) -> None:
        self.clients: dict[uuid.UUID, Client] = {}

    async def create(self, user_id: uuid.UUID, name: str) -> Client:
        client = Client(id=uuid.uuid4(), user_id=user_id, name=name, created_at=datetime.now(UTC))
        self.clients[client.id] = client
        return client

    async def list_by_user(self, user_id: uuid.UUID) -> list[Client]:
        return [c for c in self.clients.values() if c.user_id == user_id]

    async def get(self, client_id: uuid.UUID) -> Client | None:
        return self.clients.get(client_id)

    async def update(
        self,
        client_id: uuid.UUID,
        *,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        notes: str | None = None,
        logo_file_id: str | None = None,
    ) -> Client:
        client = self.clients.get(client_id)
        if client is None:
            raise NotFoundError("Client not found", details={"client_id": str(client_id)})
        if name is not None:
            client.name = name
        if email is not None:
            client.email = email
        if phone is not None:
            client.phone = phone
        if notes is not None:
            client.notes = notes
        if logo_file_id is not None:
            client.logo_file_id = logo_file_id
        return client

    async def delete(self, client_id: uuid.UUID) -> None:
        if client_id not in self.clients:
            raise NotFoundError("Client not found", details={"client_id": str(client_id)})
        del self.clients[client_id]

    async def count(self, user_id: uuid.UUID) -> int:
        return len([c for c in self.clients.values() if c.user_id == user_id])


class FakeClientLogoStorage(ClientLogoStoragePort):
    def __init__(self) -> None:
        self.files: dict[str, tuple[bytes, str]] = {}
        self._next_id = 0

    async def upload(
        self, user_id: uuid.UUID, filename: str, content: bytes, mime_type: str
    ) -> str:
        self._next_id += 1
        file_id = f"fake-logo-{self._next_id}"
        self.files[file_id] = (content, mime_type)
        return file_id

    async def download(self, user_id: uuid.UUID, file_id: str) -> tuple[bytes, str]:
        return self.files[file_id]

    async def delete(self, user_id: uuid.UUID, file_id: str) -> None:
        self.files.pop(file_id, None)


class FakeClientAttachmentRepository(ClientAttachmentRepositoryPort):
    def __init__(self) -> None:
        self.attachments: dict[uuid.UUID, ClientAttachment] = {}

    async def create(
        self,
        user_id: uuid.UUID,
        client_id: uuid.UUID,
        file_id: str,
        filename: str,
        mime_type: str,
    ) -> ClientAttachment:
        attachment = ClientAttachment(
            id=uuid.uuid4(),
            user_id=user_id,
            client_id=client_id,
            file_id=file_id,
            filename=filename,
            mime_type=mime_type,
            created_at=datetime.now(UTC),
        )
        self.attachments[attachment.id] = attachment
        return attachment

    async def list_by_client(self, client_id: uuid.UUID) -> list[ClientAttachment]:
        return [a for a in self.attachments.values() if a.client_id == client_id]

    async def get(self, attachment_id: uuid.UUID) -> ClientAttachment | None:
        return self.attachments.get(attachment_id)

    async def delete(self, attachment_id: uuid.UUID) -> None:
        if attachment_id not in self.attachments:
            raise NotFoundError(
                "Attachment not found", details={"attachment_id": str(attachment_id)}
            )
        del self.attachments[attachment_id]


class FakeProjectRepository(ProjectRepositoryPort):
    def __init__(self, clients: FakeClientRepository | None = None) -> None:
        self.projects: dict[uuid.UUID, Project] = {}
        self._clients = clients
        self.last_task_titles: dict[uuid.UUID, str] = {}

    def _client_name(self, project: Project) -> str | None:
        if project.client_id is None or self._clients is None:
            return None
        client = self._clients.clients.get(project.client_id)
        return client.name if client is not None else None

    async def create(
        self,
        user_id: uuid.UUID,
        name: str,
        client_id: uuid.UUID | None,
        type: ProjectType = ProjectType.CONSULTING,
    ) -> Project:
        now = datetime.now(UTC)
        project = Project(
            id=uuid.uuid4(),
            user_id=user_id,
            client_id=client_id,
            name=name,
            type=type,
            created_at=now,
            updated_at=now,
        )
        self.projects[project.id] = project
        return project

    async def list_by_user(self, user_id: uuid.UUID) -> list[ProjectSummary]:
        return [
            ProjectSummary(
                project=p,
                client_name=self._client_name(p),
                last_task_title=self.last_task_titles.get(p.id),
            )
            for p in self.projects.values()
            if p.user_id == user_id
        ]

    async def get(self, project_id: uuid.UUID) -> Project | None:
        return self.projects.get(project_id)

    async def get_summary(self, project_id: uuid.UUID) -> ProjectSummary | None:
        project = self.projects.get(project_id)
        if project is None:
            return None
        return ProjectSummary(
            project=project,
            client_name=self._client_name(project),
            last_task_title=self.last_task_titles.get(project_id),
        )

    async def update_type(self, project_id: uuid.UUID, type: ProjectType) -> Project:
        project = self.projects.get(project_id)
        if project is None:
            raise NotFoundError("Project not found", details={"project_id": str(project_id)})
        project.type = type
        return project

    async def count_active(self, user_id: uuid.UUID) -> int:
        return sum(1 for p in self.projects.values() if p.user_id == user_id)

    async def assign_client(self, project_id: uuid.UUID, client_id: uuid.UUID) -> Project:
        project = self.projects.get(project_id)
        if project is None:
            raise NotFoundError("Project not found", details={"project_id": str(project_id)})
        project.client_id = client_id
        return project

    async def delete(self, project_id: uuid.UUID) -> None:
        if project_id not in self.projects:
            raise NotFoundError("Project not found", details={"project_id": str(project_id)})
        del self.projects[project_id]


class FakeTaskRepository(TaskRepositoryPort):
    def __init__(self) -> None:
        self.tasks: dict[uuid.UUID, Task] = {}

    async def create(
        self,
        user_id: uuid.UUID,
        title: str,
        project_id: uuid.UUID | None = None,
        due_at: datetime | None = None,
        client_id: uuid.UUID | None = None,
        start_at: datetime | None = None,
    ) -> Task:
        now = datetime.now(UTC)
        task = Task(
            id=uuid.uuid4(),
            user_id=user_id,
            project_id=project_id,
            title=title,
            status=TaskStatus.OPEN,
            created_at=now,
            updated_at=now,
            due_at=due_at,
            client_id=client_id,
            start_at=start_at,
        )
        self.tasks[task.id] = task
        return task

    async def list_by_user(self, user_id: uuid.UUID) -> list[Task]:
        return [t for t in self.tasks.values() if t.user_id == user_id]

    async def get(self, task_id: uuid.UUID) -> Task | None:
        return self.tasks.get(task_id)

    async def update_status(self, task_id: uuid.UUID, status: TaskStatus) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        task.status = status
        return task

    async def set_due_at(self, task_id: uuid.UUID, due_at: datetime | None) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        task.due_at = due_at
        return task

    async def start_timer(self, task_id: uuid.UUID) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        task.timer_started_at = datetime.now(UTC)
        task.status = TaskStatus.IN_PROGRESS
        return task

    async def stop_timer(self, task_id: uuid.UUID) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        task.timer_started_at = None
        task.status = TaskStatus.OPEN
        return task

    async def update_details(
        self,
        task_id: uuid.UUID,
        title: str,
        due_at: datetime | None,
        project_id: uuid.UUID | None,
        client_id: uuid.UUID | None,
        start_at: datetime | None = None,
    ) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        task.title = title
        task.due_at = due_at
        task.project_id = project_id
        task.client_id = client_id
        task.start_at = start_at
        return task

    async def delete(self, task_id: uuid.UUID) -> None:
        if task_id not in self.tasks:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        del self.tasks[task_id]

    async def count_open(self, user_id: uuid.UUID) -> int:
        return sum(
            1
            for t in self.tasks.values()
            if t.user_id == user_id and t.status != TaskStatus.DONE
        )

    async def set_daily_attributes(
        self,
        task_id: uuid.UUID,
        deliverable: str,
        estimated_minutes: int,
        importance: TaskImportance,
        goal_id: uuid.UUID | None,
    ) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        task.deliverable = deliverable
        task.estimated_minutes = estimated_minutes
        task.importance = importance
        task.goal_id = goal_id
        return task

    async def set_next_step(self, task_id: uuid.UUID, next_step: str | None) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task not found", details={"task_id": str(task_id)})
        task.next_step = next_step
        return task


class FakeGoalRepository(GoalRepositoryPort):
    def __init__(self) -> None:
        self.goals: dict[uuid.UUID, Goal] = {}

    async def create(self, user_id: uuid.UUID, name: str) -> Goal:
        goal = Goal(id=uuid.uuid4(), user_id=user_id, name=name, created_at=datetime.now(UTC))
        self.goals[goal.id] = goal
        return goal

    async def list_by_user(self, user_id: uuid.UUID) -> list[Goal]:
        return [g for g in self.goals.values() if g.user_id == user_id]

    async def get(self, goal_id: uuid.UUID) -> Goal | None:
        return self.goals.get(goal_id)

    async def update(self, goal_id: uuid.UUID, name: str) -> Goal:
        goal = self.goals.get(goal_id)
        if goal is None:
            raise NotFoundError("Goal not found", details={"goal_id": str(goal_id)})
        goal.name = name
        return goal

    async def delete(self, goal_id: uuid.UUID) -> None:
        if goal_id not in self.goals:
            raise NotFoundError("Goal not found", details={"goal_id": str(goal_id)})
        del self.goals[goal_id]


class FakeDailyPlanRepository(DailyPlanRepositoryPort):
    def __init__(self) -> None:
        self.plans: dict[uuid.UUID, DailyPlan] = {}

    async def get_by_date(self, user_id: uuid.UUID, plan_date: date) -> DailyPlan | None:
        for plan in self.plans.values():
            if plan.user_id == user_id and plan.plan_date == plan_date:
                return plan
        return None

    async def create(self, user_id: uuid.UUID, plan_date: date) -> DailyPlan:
        now = datetime.now(UTC)
        plan = DailyPlan(
            id=uuid.uuid4(),
            user_id=user_id,
            plan_date=plan_date,
            main_task_id=None,
            secondary_task_id_1=None,
            secondary_task_id_2=None,
            is_locked=False,
            locked_at=None,
            carry_over_task_id=None,
            created_at=now,
            updated_at=now,
        )
        self.plans[plan.id] = plan
        return plan

    async def get(self, daily_plan_id: uuid.UUID) -> DailyPlan | None:
        return self.plans.get(daily_plan_id)

    async def set_main_task(
        self, daily_plan_id: uuid.UUID, task_id: uuid.UUID | None
    ) -> DailyPlan:
        plan = self._get_or_raise(daily_plan_id)
        plan.main_task_id = task_id
        return plan

    async def set_secondary_task(
        self, daily_plan_id: uuid.UUID, slot: int, task_id: uuid.UUID | None
    ) -> DailyPlan:
        plan = self._get_or_raise(daily_plan_id)
        if slot == 1:
            plan.secondary_task_id_1 = task_id
        elif slot == 2:
            plan.secondary_task_id_2 = task_id
        else:
            raise ValueError("slot must be 1 or 2")
        return plan

    async def lock(self, daily_plan_id: uuid.UUID) -> DailyPlan:
        plan = self._get_or_raise(daily_plan_id)
        plan.is_locked = True
        plan.locked_at = datetime.now(UTC)
        return plan

    async def set_carry_over(
        self, daily_plan_id: uuid.UUID, task_id: uuid.UUID | None
    ) -> DailyPlan:
        plan = self._get_or_raise(daily_plan_id)
        plan.carry_over_task_id = task_id
        return plan

    async def list_by_user_between(
        self, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[DailyPlan]:
        return [
            p
            for p in self.plans.values()
            if p.user_id == user_id and start_date <= p.plan_date < end_date
        ]

    def _get_or_raise(self, daily_plan_id: uuid.UUID) -> DailyPlan:
        plan = self.plans.get(daily_plan_id)
        if plan is None:
            raise NotFoundError(
                "Daily plan not found", details={"daily_plan_id": str(daily_plan_id)}
            )
        return plan


class FakeFocusSessionRepository(FocusSessionRepositoryPort):
    def __init__(self) -> None:
        self.sessions: dict[uuid.UUID, FocusSession] = {}

    async def start(
        self, user_id: uuid.UUID, task_id: uuid.UUID, daily_plan_id: uuid.UUID
    ) -> FocusSession:
        session = FocusSession(
            id=uuid.uuid4(),
            user_id=user_id,
            task_id=task_id,
            daily_plan_id=daily_plan_id,
            started_at=datetime.now(UTC),
        )
        self.sessions[session.id] = session
        return session

    async def end(
        self,
        session_id: uuid.UUID,
        exit_reason: FocusExitReason,
        stuck_reason: FocusStuckReason | None,
    ) -> FocusSession:
        session = self.sessions.get(session_id)
        if session is None:
            raise NotFoundError(
                "Focus session not found", details={"session_id": str(session_id)}
            )
        session.ended_at = datetime.now(UTC)
        session.exit_reason = exit_reason
        session.stuck_reason = stuck_reason
        return session

    async def get(self, session_id: uuid.UUID) -> FocusSession | None:
        return self.sessions.get(session_id)

    async def get_active_by_user(self, user_id: uuid.UUID) -> FocusSession | None:
        for session in self.sessions.values():
            if session.user_id == user_id and session.ended_at is None:
                return session
        return None

    async def list_by_daily_plan(self, daily_plan_id: uuid.UUID) -> list[FocusSession]:
        return [s for s in self.sessions.values() if s.daily_plan_id == daily_plan_id]

    async def list_by_user_between(
        self, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[FocusSession]:
        return [
            s
            for s in self.sessions.values()
            if s.user_id == user_id and start_date <= s.started_at.date() < end_date
        ]


class FakeDailyPlanSwapRepository(DailyPlanSwapRepositoryPort):
    def __init__(self) -> None:
        self.swaps: dict[uuid.UUID, DailyPlanSwap] = {}

    async def create(
        self,
        user_id: uuid.UUID,
        daily_plan_id: uuid.UUID,
        bumped_task_id: uuid.UUID,
        new_task_id: uuid.UUID,
    ) -> DailyPlanSwap:
        swap = DailyPlanSwap(
            id=uuid.uuid4(),
            user_id=user_id,
            daily_plan_id=daily_plan_id,
            bumped_task_id=bumped_task_id,
            new_task_id=new_task_id,
            created_at=datetime.now(UTC),
        )
        self.swaps[swap.id] = swap
        return swap

    async def list_by_daily_plan(self, daily_plan_id: uuid.UUID) -> list[DailyPlanSwap]:
        return [s for s in self.swaps.values() if s.daily_plan_id == daily_plan_id]

    async def list_by_user_between(
        self, user_id: uuid.UUID, start_date: date, end_date: date
    ) -> list[DailyPlanSwap]:
        return [
            s
            for s in self.swaps.values()
            if s.user_id == user_id and start_date <= s.created_at.date() < end_date
        ]


class FakeThoughtRepository(ThoughtRepositoryPort):
    def __init__(self) -> None:
        self.thoughts: dict[uuid.UUID, Thought] = {}

    async def create(self, user_id: uuid.UUID, content: str) -> Thought:
        thought = Thought(
            id=uuid.uuid4(), user_id=user_id, content=content, created_at=datetime.now(UTC)
        )
        self.thoughts[thought.id] = thought
        return thought

    async def list_by_user(self, user_id: uuid.UUID) -> list[Thought]:
        return [t for t in self.thoughts.values() if t.user_id == user_id]

    async def get(self, thought_id: uuid.UUID) -> Thought | None:
        return self.thoughts.get(thought_id)

    async def delete(self, thought_id: uuid.UUID) -> None:
        if thought_id not in self.thoughts:
            raise NotFoundError("Thought not found", details={"thought_id": str(thought_id)})
        del self.thoughts[thought_id]


class FakeWhatsAppMessageRepository(WhatsAppMessageRepositoryPort):
    def __init__(self) -> None:
        self.messages: list[WhatsAppMessage] = []

    async def create(
        self,
        user_id: uuid.UUID,
        phone_number: str,
        direction: WhatsAppDirection,
        content: str,
    ) -> WhatsAppMessage:
        message = WhatsAppMessage(
            id=uuid.uuid4(),
            user_id=user_id,
            phone_number=phone_number,
            direction=direction,
            content=content,
            created_at=datetime.now(UTC),
        )
        self.messages.append(message)
        return message

    async def list_by_phone_number(
        self, user_id: uuid.UUID, phone_number: str, limit: int = 50
    ) -> list[WhatsAppMessage]:
        matches = [
            m
            for m in self.messages
            if m.user_id == user_id and m.phone_number == phone_number
        ]
        return matches[-limit:]


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

    async def list_all(self) -> list[User]:
        return list(self.users.values())


class FakeNotificationRepository(NotificationRepositoryPort):
    def __init__(self) -> None:
        self.notifications: dict[uuid.UUID, Notification] = {}

    async def create(
        self,
        user_id: uuid.UUID,
        kind: NotificationKind,
        related_id: uuid.UUID,
        title: str,
        body: str,
    ) -> Notification:
        notification = Notification(
            id=uuid.uuid4(),
            user_id=user_id,
            kind=kind,
            related_id=related_id,
            title=title,
            body=body,
            created_at=datetime.now(UTC),
        )
        self.notifications[notification.id] = notification
        return notification

    async def exists(
        self, user_id: uuid.UUID, kind: NotificationKind, related_id: uuid.UUID
    ) -> bool:
        return any(
            n.user_id == user_id and n.kind == kind and n.related_id == related_id
            for n in self.notifications.values()
        )

    async def get(self, notification_id: uuid.UUID) -> Notification | None:
        return self.notifications.get(notification_id)

    async def list_unread(self, user_id: uuid.UUID) -> list[Notification]:
        return [
            n for n in self.notifications.values() if n.user_id == user_id and n.read_at is None
        ]

    async def mark_read(self, notification_id: uuid.UUID) -> Notification:
        notification = self.notifications.get(notification_id)
        if notification is None:
            raise NotFoundError(
                "Notification not found", details={"notification_id": str(notification_id)}
            )
        notification.read_at = datetime.now(UTC)
        return notification

    async def mark_all_read(self, user_id: uuid.UUID) -> None:
        now = datetime.now(UTC)
        for n in self.notifications.values():
            if n.user_id == user_id and n.read_at is None:
                n.read_at = now


class FakeCalendarPort(CalendarPort):
    def __init__(self, *, fail_with: type[AppError] | None = None) -> None:
        self.events: dict[str, CalendarEvent] = {}
        self._fail_with = fail_with

    async def list_between(
        self, user_id: uuid.UUID, time_min: str, time_max: str
    ) -> list[CalendarEvent]:
        if self._fail_with is not None:
            raise self._fail_with("Calendar is unavailable")
        return list(self.events.values())

    async def create(
        self,
        user_id: uuid.UUID,
        summary: str,
        start_time: str,
        end_time: str,
        description: str | None = None,
    ) -> CalendarEvent:
        event = CalendarEvent(
            id=str(uuid.uuid4()), summary=summary, start=start_time, end=end_time,
            description=description,
        )
        self.events[event.id] = event
        return event

    async def delete(self, user_id: uuid.UUID, event_id: str) -> None:
        self.events.pop(event_id, None)


class FakeGreenInvoicePort(GreenInvoicePort):
    def __init__(self, *, fail_with: type[AppError] | None = None) -> None:
        self.income: list[IncomeRecord] = []
        self.expenses: list[ExpenseRecord] = []
        self._fail_with = fail_with

    async def list_income(self, from_date: date, to_date: date) -> list[IncomeRecord]:
        if self._fail_with is not None:
            raise self._fail_with("Green Invoice is unavailable")
        return self.income

    async def list_expenses(self, from_date: date, to_date: date) -> list[ExpenseRecord]:
        if self._fail_with is not None:
            raise self._fail_with("Green Invoice is unavailable")
        return self.expenses


class FakeCache(CachePort):
    def __init__(self) -> None:
        self.store: dict[str, str] = {}

    async def get(self, key: str) -> str | None:
        return self.store.get(key)

    async def set(self, key: str, value: str, ttl_seconds: int | None = None) -> None:
        self.store[key] = value

    async def delete(self, key: str) -> None:
        self.store.pop(key, None)


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


@pytest.fixture
def fake_client_repository() -> FakeClientRepository:
    return FakeClientRepository()


@pytest.fixture
def fake_client_logo_storage() -> FakeClientLogoStorage:
    return FakeClientLogoStorage()


@pytest.fixture
def fake_client_attachment_repository() -> FakeClientAttachmentRepository:
    return FakeClientAttachmentRepository()


@pytest.fixture
def fake_project_repository(
    fake_client_repository: FakeClientRepository,
) -> FakeProjectRepository:
    return FakeProjectRepository(fake_client_repository)


@pytest.fixture
def fake_task_repository() -> FakeTaskRepository:
    return FakeTaskRepository()


@pytest.fixture
def fake_thought_repository() -> FakeThoughtRepository:
    return FakeThoughtRepository()


@pytest.fixture
def fake_whatsapp_message_repository() -> FakeWhatsAppMessageRepository:
    return FakeWhatsAppMessageRepository()


@pytest.fixture
def fake_notification_repository() -> FakeNotificationRepository:
    return FakeNotificationRepository()


@pytest.fixture
def fake_calendar_port() -> FakeCalendarPort:
    return FakeCalendarPort()


@pytest.fixture
def fake_goal_repository() -> FakeGoalRepository:
    return FakeGoalRepository()


@pytest.fixture
def fake_daily_plan_repository() -> FakeDailyPlanRepository:
    return FakeDailyPlanRepository()


@pytest.fixture
def fake_focus_session_repository() -> FakeFocusSessionRepository:
    return FakeFocusSessionRepository()


@pytest.fixture
def fake_daily_plan_swap_repository() -> FakeDailyPlanSwapRepository:
    return FakeDailyPlanSwapRepository()
