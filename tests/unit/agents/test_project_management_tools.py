from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any

from app.agents.project_management.tools import (
    AssignProjectToClientTool,
    AssignTaskToClientTool,
    BulkCreateTasksTool,
    CreateClientTool,
    CreateProjectTool,
    CreateTaskTool,
    CreateThoughtTool,
    DeleteClientTool,
    DeleteProjectTool,
    DeleteTaskTool,
    GetClientDetailTool,
    ListProjectsTool,
    ListTasksTool,
    SetTaskDueDateTool,
    UpdateClientTool,
    UpdateProjectTypeTool,
    UpdateTaskStatusTool,
)
from app.application.ports.agent_tool import ToolExecutionContext
from app.core.exceptions import ValidationError
from app.domain.entities import (
    Client,
    ClientDetail,
    Project,
    ProjectSummary,
    ProjectType,
    Task,
    TaskCategory,
    TaskStatus,
    Thought,
)


class _FakeWorkspaceService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def create_client(self, user_id: uuid.UUID, name: str) -> Client:
        self.calls.append(("create_client", (user_id, name)))
        return Client(id=uuid.uuid4(), user_id=user_id, name=name, created_at=datetime.now(UTC))

    async def update_client(
        self,
        user_id: uuid.UUID,
        client_name: str,
        *,
        email: str | None = None,
        phone: str | None = None,
        notes: str | None = None,
    ) -> Client:
        self.calls.append(("update_client", (user_id, client_name, email, phone, notes)))
        return Client(
            id=uuid.uuid4(),
            user_id=user_id,
            name=client_name,
            created_at=datetime.now(UTC),
            email=email,
            phone=phone,
            notes=notes,
        )

    async def delete_client(self, user_id: uuid.UUID, client_name: str) -> None:
        self.calls.append(("delete_client", (user_id, client_name)))

    async def get_client_detail(self, user_id: uuid.UUID, client_name: str) -> ClientDetail:
        self.calls.append(("get_client_detail", (user_id, client_name)))
        client = Client(
            id=uuid.uuid4(), user_id=user_id, name=client_name, created_at=datetime.now(UTC)
        )
        return ClientDetail(client=client, projects=[], tasks=[], attachments=[])

    async def create_project(
        self,
        user_id: uuid.UUID,
        name: str,
        client_name: str | None = None,
        type: ProjectType | None = None,
    ) -> Project:
        self.calls.append(("create_project", (user_id, name, client_name, type)))
        now = datetime.now(UTC)
        return Project(
            id=uuid.uuid4(),
            user_id=user_id,
            client_id=None,
            name=name,
            type=type or ProjectType.CONSULTING,
            created_at=now,
            updated_at=now,
        )

    async def update_project_type(
        self, user_id: uuid.UUID, project_name: str, type: ProjectType
    ) -> Project:
        self.calls.append(("update_project_type", (user_id, project_name, type)))
        now = datetime.now(UTC)
        return Project(
            id=uuid.uuid4(),
            user_id=user_id,
            client_id=None,
            name=project_name,
            type=type,
            created_at=now,
            updated_at=now,
        )

    async def assign_project_client(
        self, user_id: uuid.UUID, project_name: str, client_name: str
    ) -> Project:
        self.calls.append(("assign_project_client", (user_id, project_name, client_name)))
        now = datetime.now(UTC)
        return Project(
            id=uuid.uuid4(),
            user_id=user_id,
            client_id=uuid.uuid4(),
            name=project_name,
            type=ProjectType.CONSULTING,
            created_at=now,
            updated_at=now,
        )

    async def delete_project(self, user_id: uuid.UUID, project_name: str) -> None:
        self.calls.append(("delete_project", (user_id, project_name)))

    async def list_projects(self, user_id: uuid.UUID) -> list[ProjectSummary]:
        self.calls.append(("list_projects", (user_id,)))
        now = datetime.now(UTC)
        project = Project(
            id=uuid.uuid4(),
            user_id=user_id,
            client_id=None,
            name="Summer menu",
            type=ProjectType.CONSULTING,
            created_at=now,
            updated_at=now,
        )
        return [ProjectSummary(project=project, client_name="Baron's", last_task_title=None)]

    async def create_task(
        self,
        user_id: uuid.UUID,
        title: str,
        project_name: str | None = None,
        due_at: datetime | None = None,
        client_name: str | None = None,
        start_at: datetime | None = None,
        category: TaskCategory | None = None,
    ) -> Task:
        self.calls.append(
            (
                "create_task",
                (user_id, title, project_name, due_at, client_name, start_at, category),
            )
        )
        now = datetime.now(UTC)
        return Task(
            id=uuid.uuid4(),
            user_id=user_id,
            project_id=None,
            client_id=uuid.uuid4() if client_name else None,
            title=title,
            status=TaskStatus.OPEN,
            created_at=now,
            updated_at=now,
            due_at=due_at,
            start_at=start_at,
            category=category,
        )

    async def bulk_quick_capture_tasks(
        self, user_id: uuid.UUID, items: list[tuple[str, datetime | None, TaskCategory]]
    ) -> list[Task]:
        self.calls.append(("bulk_quick_capture_tasks", (user_id, items)))
        now = datetime.now(UTC)
        return [
            Task(
                id=uuid.uuid4(),
                user_id=user_id,
                project_id=None,
                title=title,
                status=TaskStatus.OPEN,
                created_at=now,
                updated_at=now,
                due_at=due_at,
                category=category,
            )
            for title, due_at, category in items
        ]

    async def update_task_status(
        self, user_id: uuid.UUID, task_title: str, status: TaskStatus
    ) -> Task:
        self.calls.append(("update_task_status", (user_id, task_title, status)))
        now = datetime.now(UTC)
        return Task(
            id=uuid.uuid4(),
            user_id=user_id,
            project_id=None,
            title=task_title,
            status=status,
            created_at=now,
            updated_at=now,
        )

    async def set_task_due_at(
        self, user_id: uuid.UUID, task_title: str, due_at: datetime | None
    ) -> Task:
        self.calls.append(("set_task_due_at", (user_id, task_title, due_at)))
        now = datetime.now(UTC)
        return Task(
            id=uuid.uuid4(),
            user_id=user_id,
            project_id=None,
            title=task_title,
            status=TaskStatus.OPEN,
            created_at=now,
            updated_at=now,
            due_at=due_at,
        )

    async def delete_task(self, user_id: uuid.UUID, task_title: str) -> None:
        self.calls.append(("delete_task", (user_id, task_title)))

    async def assign_task_client(
        self, user_id: uuid.UUID, task_title: str, client_name: str | None
    ) -> Task:
        self.calls.append(("assign_task_client", (user_id, task_title, client_name)))
        now = datetime.now(UTC)
        return Task(
            id=uuid.uuid4(),
            user_id=user_id,
            project_id=None,
            client_id=uuid.uuid4() if client_name else None,
            title=task_title,
            status=TaskStatus.OPEN,
            created_at=now,
            updated_at=now,
        )

    async def list_tasks(self, user_id: uuid.UUID) -> list[Task]:
        self.calls.append(("list_tasks", (user_id,)))
        now = datetime.now(UTC)
        return [
            Task(
                id=uuid.uuid4(),
                user_id=user_id,
                project_id=None,
                title="Prep summer menu",
                status=TaskStatus.OPEN,
                created_at=now,
                updated_at=now,
            )
        ]

    async def create_thought(self, user_id: uuid.UUID, content: str) -> Thought:
        self.calls.append(("create_thought", (user_id, content)))
        stripped = content.strip()
        if not stripped:
            raise ValidationError("A thought needs some content.")
        return Thought(
            id=uuid.uuid4(), user_id=user_id, content=stripped, created_at=datetime.now(UTC)
        )


def _context() -> ToolExecutionContext:
    return ToolExecutionContext(
        user_id=uuid.uuid4(), conversation_id=uuid.uuid4(), correlation_id="corr"
    )


async def test_create_client_tool() -> None:
    service = _FakeWorkspaceService()
    tool = CreateClientTool(service)
    context = _context()

    result = await tool.execute({"name": "Baron's"}, context)

    assert service.calls == [("create_client", (context.user_id, "Baron's"))]
    assert json.loads(result.content)["name"] == "Baron's"


async def test_update_client_tool() -> None:
    service = _FakeWorkspaceService()
    tool = UpdateClientTool(service)
    context = _context()

    result = await tool.execute(
        {"client_name": "Baron's", "email": "baron@example.com", "notes": "VIP"}, context
    )

    assert service.calls == [
        ("update_client", (context.user_id, "Baron's", "baron@example.com", None, "VIP"))
    ]
    body = json.loads(result.content)
    assert body["email"] == "baron@example.com"
    assert body["notes"] == "VIP"


async def test_delete_client_tool() -> None:
    service = _FakeWorkspaceService()
    tool = DeleteClientTool(service)
    context = _context()

    result = await tool.execute({"client_name": "Baron's"}, context)

    assert service.calls == [("delete_client", (context.user_id, "Baron's"))]
    assert json.loads(result.content) == {"deleted": True}


async def test_get_client_detail_tool() -> None:
    service = _FakeWorkspaceService()
    tool = GetClientDetailTool(service)
    context = _context()

    result = await tool.execute({"client_name": "Baron's"}, context)

    assert service.calls == [("get_client_detail", (context.user_id, "Baron's"))]
    body = json.loads(result.content)
    assert body["client"]["name"] == "Baron's"
    assert body["projects"] == []
    assert body["tasks"] == []


async def test_create_project_tool_passes_client_name_and_type() -> None:
    service = _FakeWorkspaceService()
    tool = CreateProjectTool(service)
    context = _context()

    result = await tool.execute(
        {"name": "Summer menu", "client_name": "Baron's", "type": "consulting"}, context
    )

    assert service.calls == [
        (
            "create_project",
            (context.user_id, "Summer menu", "Baron's", ProjectType.CONSULTING),
        )
    ]
    assert json.loads(result.content)["type"] == "consulting"


async def test_assign_project_to_client_tool() -> None:
    service = _FakeWorkspaceService()
    tool = AssignProjectToClientTool(service)
    context = _context()

    result = await tool.execute({"project_name": "Summer menu", "client_name": "Baron's"}, context)

    assert service.calls == [("assign_project_client", (context.user_id, "Summer menu", "Baron's"))]
    assert json.loads(result.content)["client_id"] is not None


async def test_delete_project_tool() -> None:
    service = _FakeWorkspaceService()
    tool = DeleteProjectTool(service)
    context = _context()

    result = await tool.execute({"project_name": "Summer menu"}, context)

    assert service.calls == [("delete_project", (context.user_id, "Summer menu"))]
    assert json.loads(result.content) == {"deleted": True}


async def test_update_project_type_tool_parses_enum() -> None:
    service = _FakeWorkspaceService()
    tool = UpdateProjectTypeTool(service)
    context = _context()

    result = await tool.execute({"project_name": "Summer menu", "type": "mentoring"}, context)

    assert service.calls == [
        ("update_project_type", (context.user_id, "Summer menu", ProjectType.MENTORING))
    ]
    assert json.loads(result.content)["type"] == "mentoring"


async def test_list_projects_tool_includes_denormalized_fields() -> None:
    service = _FakeWorkspaceService()
    tool = ListProjectsTool(service)
    context = _context()

    result = await tool.execute({}, context)

    projects = json.loads(result.content)
    assert projects[0]["name"] == "Summer menu"
    assert projects[0]["client_name"] == "Baron's"


async def test_create_task_tool_passes_project_name() -> None:
    service = _FakeWorkspaceService()
    tool = CreateTaskTool(service)
    context = _context()

    await tool.execute(
        {
            "title": "Prep summer menu",
            "project_name": "Summer menu",
            "start_at": "2026-08-01T08:00:00+00:00",
            "due_at": "2026-08-01T09:00:00+00:00",
            "category": "operational",
        },
        context,
    )

    assert service.calls == [
        (
            "create_task",
            (
                context.user_id,
                "Prep summer menu",
                "Summer menu",
                datetime(2026, 8, 1, 9, 0, tzinfo=UTC),
                None,
                datetime(2026, 8, 1, 8, 0, tzinfo=UTC),
                TaskCategory.OPERATIONAL,
            ),
        )
    ]


async def test_create_task_tool_parses_start_and_due_at() -> None:
    service = _FakeWorkspaceService()
    tool = CreateTaskTool(service)
    context = _context()

    result = await tool.execute(
        {
            "title": "Send invoice",
            "start_at": "2026-08-01T08:00:00+00:00",
            "due_at": "2026-08-01T09:00:00+00:00",
            "category": "managerial",
        },
        context,
    )

    assert service.calls == [
        (
            "create_task",
            (
                context.user_id,
                "Send invoice",
                None,
                datetime(2026, 8, 1, 9, 0, tzinfo=UTC),
                None,
                datetime(2026, 8, 1, 8, 0, tzinfo=UTC),
                TaskCategory.MANAGERIAL,
            ),
        )
    ]
    assert json.loads(result.content)["due_at"] == "2026-08-01T09:00:00+00:00"
    assert json.loads(result.content)["start_at"] == "2026-08-01T08:00:00+00:00"


async def test_create_task_tool_passes_client_name() -> None:
    service = _FakeWorkspaceService()
    tool = CreateTaskTool(service)
    context = _context()

    result = await tool.execute(
        {
            "title": "Kickoff call",
            "client_name": "Baron's",
            "start_at": "2026-08-01T08:00:00+00:00",
            "due_at": "2026-08-01T09:00:00+00:00",
            "category": "operational",
        },
        context,
    )

    assert service.calls == [
        (
            "create_task",
            (
                context.user_id,
                "Kickoff call",
                None,
                datetime(2026, 8, 1, 9, 0, tzinfo=UTC),
                "Baron's",
                datetime(2026, 8, 1, 8, 0, tzinfo=UTC),
                TaskCategory.OPERATIONAL,
            ),
        )
    ]
    assert json.loads(result.content)["client_id"] is not None


async def test_bulk_create_tasks_tool_parses_titles_and_due_dates() -> None:
    service = _FakeWorkspaceService()
    tool = BulkCreateTasksTool(service)
    context = _context()

    result = await tool.execute(
        {
            "tasks": [
                {
                    "title": "Send contract to lawyer",
                    "due_date": "2026-07-27",
                    "category": "managerial",
                },
                {"title": "Set final pricing", "category": "operational"},
            ]
        },
        context,
    )

    assert service.calls == [
        (
            "bulk_quick_capture_tasks",
            (
                context.user_id,
                [
                    (
                        "Send contract to lawyer",
                        datetime(2026, 7, 27, 0, 0),
                        TaskCategory.MANAGERIAL,
                    ),
                    ("Set final pricing", None, TaskCategory.OPERATIONAL),
                ],
            ),
        )
    ]
    parsed = json.loads(result.content)
    assert len(parsed) == 2
    assert parsed[0]["title"] == "Send contract to lawyer"


async def test_set_task_due_date_tool() -> None:
    service = _FakeWorkspaceService()
    tool = SetTaskDueDateTool(service)
    context = _context()

    result = await tool.execute(
        {"task_title": "Send invoice", "due_at": "2026-09-01T09:00:00+00:00"}, context
    )

    assert service.calls == [
        (
            "set_task_due_at",
            (context.user_id, "Send invoice", datetime(2026, 9, 1, 9, 0, tzinfo=UTC)),
        )
    ]
    assert json.loads(result.content)["due_at"] == "2026-09-01T09:00:00+00:00"


async def test_set_task_due_date_tool_clears_due_date_when_omitted() -> None:
    service = _FakeWorkspaceService()
    tool = SetTaskDueDateTool(service)
    context = _context()

    await tool.execute({"task_title": "Send invoice"}, context)

    assert service.calls == [("set_task_due_at", (context.user_id, "Send invoice", None))]


async def test_update_task_status_tool_parses_enum() -> None:
    service = _FakeWorkspaceService()
    tool = UpdateTaskStatusTool(service)
    context = _context()

    result = await tool.execute({"task_title": "Prep summer menu", "status": "done"}, context)

    assert service.calls == [
        ("update_task_status", (context.user_id, "Prep summer menu", TaskStatus.DONE))
    ]
    assert json.loads(result.content)["status"] == "done"


async def test_delete_task_tool() -> None:
    service = _FakeWorkspaceService()
    tool = DeleteTaskTool(service)
    context = _context()

    result = await tool.execute({"task_title": "Prep summer menu"}, context)

    assert service.calls == [("delete_task", (context.user_id, "Prep summer menu"))]
    assert json.loads(result.content) == {"deleted": True}


async def test_assign_task_to_client_tool() -> None:
    service = _FakeWorkspaceService()
    tool = AssignTaskToClientTool(service)
    context = _context()

    result = await tool.execute(
        {"task_title": "Prep summer menu", "client_name": "Baron's"}, context
    )

    assert service.calls == [
        ("assign_task_client", (context.user_id, "Prep summer menu", "Baron's"))
    ]
    assert json.loads(result.content)["client_id"] is not None


async def test_assign_task_to_client_tool_clears_when_omitted() -> None:
    service = _FakeWorkspaceService()
    tool = AssignTaskToClientTool(service)
    context = _context()

    result = await tool.execute({"task_title": "Prep summer menu"}, context)

    assert service.calls == [("assign_task_client", (context.user_id, "Prep summer menu", None))]
    assert json.loads(result.content)["client_id"] is None


async def test_list_tasks_tool() -> None:
    service = _FakeWorkspaceService()
    tool = ListTasksTool(service)
    context = _context()

    result = await tool.execute({}, context)

    tasks = json.loads(result.content)
    assert tasks[0]["title"] == "Prep summer menu"


async def test_create_thought_tool() -> None:
    service = _FakeWorkspaceService()
    tool = CreateThoughtTool(service)
    context = _context()

    result = await tool.execute({"content": "call the accountant tomorrow"}, context)

    assert service.calls == [("create_thought", (context.user_id, "call the accountant tomorrow"))]
    assert json.loads(result.content)["content"] == "call the accountant tomorrow"
