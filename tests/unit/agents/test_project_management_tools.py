from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any

from app.agents.project_management.tools import (
    CreateClientTool,
    CreateProjectTool,
    CreateTaskTool,
    ListProjectsTool,
    ListTasksTool,
    UpdateProjectStatusTool,
    UpdateTaskStatusTool,
)
from app.application.ports.agent_tool import ToolExecutionContext
from app.domain.entities import (
    Client,
    Project,
    ProjectStatus,
    ProjectSummary,
    Task,
    TaskStatus,
)


class _FakeWorkspaceService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def create_client(self, user_id: uuid.UUID, name: str) -> Client:
        self.calls.append(("create_client", (user_id, name)))
        return Client(id=uuid.uuid4(), user_id=user_id, name=name, created_at=datetime.now(UTC))

    async def create_project(
        self, user_id: uuid.UUID, name: str, client_name: str | None = None
    ) -> Project:
        self.calls.append(("create_project", (user_id, name, client_name)))
        now = datetime.now(UTC)
        return Project(
            id=uuid.uuid4(),
            user_id=user_id,
            client_id=None,
            name=name,
            status=ProjectStatus.IN_PROGRESS,
            created_at=now,
            updated_at=now,
        )

    async def update_project_status(
        self, user_id: uuid.UUID, project_name: str, status: ProjectStatus
    ) -> Project:
        self.calls.append(("update_project_status", (user_id, project_name, status)))
        now = datetime.now(UTC)
        return Project(
            id=uuid.uuid4(),
            user_id=user_id,
            client_id=None,
            name=project_name,
            status=status,
            created_at=now,
            updated_at=now,
        )

    async def list_projects(self, user_id: uuid.UUID) -> list[ProjectSummary]:
        self.calls.append(("list_projects", (user_id,)))
        now = datetime.now(UTC)
        project = Project(
            id=uuid.uuid4(),
            user_id=user_id,
            client_id=None,
            name="Summer menu",
            status=ProjectStatus.IN_PROGRESS,
            created_at=now,
            updated_at=now,
        )
        return [ProjectSummary(project=project, client_name="Baron's", last_task_title=None)]

    async def create_task(
        self, user_id: uuid.UUID, title: str, project_name: str | None = None
    ) -> Task:
        self.calls.append(("create_task", (user_id, title, project_name)))
        now = datetime.now(UTC)
        return Task(
            id=uuid.uuid4(),
            user_id=user_id,
            project_id=None,
            title=title,
            status=TaskStatus.OPEN,
            created_at=now,
            updated_at=now,
        )

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


async def test_create_project_tool_passes_client_name() -> None:
    service = _FakeWorkspaceService()
    tool = CreateProjectTool(service)
    context = _context()

    result = await tool.execute({"name": "Summer menu", "client_name": "Baron's"}, context)

    assert service.calls == [("create_project", (context.user_id, "Summer menu", "Baron's"))]
    assert json.loads(result.content)["status"] == "in_progress"


async def test_update_project_status_tool_parses_enum() -> None:
    service = _FakeWorkspaceService()
    tool = UpdateProjectStatusTool(service)
    context = _context()

    result = await tool.execute(
        {"project_name": "Summer menu", "status": "on_hold"}, context
    )

    assert service.calls == [
        ("update_project_status", (context.user_id, "Summer menu", ProjectStatus.ON_HOLD))
    ]
    assert json.loads(result.content)["status"] == "on_hold"


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

    await tool.execute({"title": "Prep summer menu", "project_name": "Summer menu"}, context)

    assert service.calls == [
        ("create_task", (context.user_id, "Prep summer menu", "Summer menu"))
    ]


async def test_update_task_status_tool_parses_enum() -> None:
    service = _FakeWorkspaceService()
    tool = UpdateTaskStatusTool(service)
    context = _context()

    result = await tool.execute(
        {"task_title": "Prep summer menu", "status": "done"}, context
    )

    assert service.calls == [
        ("update_task_status", (context.user_id, "Prep summer menu", TaskStatus.DONE))
    ]
    assert json.loads(result.content)["status"] == "done"


async def test_list_tasks_tool() -> None:
    service = _FakeWorkspaceService()
    tool = ListTasksTool(service)
    context = _context()

    result = await tool.execute({}, context)

    tasks = json.loads(result.content)
    assert tasks[0]["title"] == "Prep summer menu"
