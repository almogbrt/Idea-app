from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from app.agents.project_management.service import WorkspaceService
from app.application.ports.agent_tool import Tool, ToolExecutionContext
from app.domain.entities import (
    Client,
    ClientDetail,
    Project,
    ProjectStatus,
    ProjectSummary,
    Task,
    TaskStatus,
    ToolResult,
)

AGENT_NAME = "project_management"


def _parse_due_at(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def _client_json(client: Client) -> dict[str, Any]:
    return {
        "id": str(client.id),
        "name": client.name,
        "email": client.email,
        "phone": client.phone,
        "notes": client.notes,
        "next_follow_up_at": client.next_follow_up_at.isoformat()
        if client.next_follow_up_at
        else None,
    }


def _project_json(project: Project) -> dict[str, Any]:
    return {
        "id": str(project.id),
        "name": project.name,
        "status": project.status.value,
        "client_id": str(project.client_id) if project.client_id else None,
    }


def _project_summary_json(summary: ProjectSummary) -> dict[str, Any]:
    data = _project_json(summary.project)
    data["client_name"] = summary.client_name
    data["last_task_title"] = summary.last_task_title
    return data


def _task_json(task: Task) -> dict[str, Any]:
    return {
        "id": str(task.id),
        "title": task.title,
        "status": task.status.value,
        "project_id": str(task.project_id) if task.project_id else None,
        "due_at": task.due_at.isoformat() if task.due_at else None,
    }


def _client_detail_json(detail: ClientDetail) -> dict[str, Any]:
    return {
        "client": _client_json(detail.client),
        "projects": [_project_summary_json(s) for s in detail.projects],
        "tasks": [_task_json(t) for t in detail.tasks],
    }


class CreateClientTool(Tool):
    name = "workspace_create_client"
    description = (
        "Create a new client record (or return the existing one if a client with a "
        "similar name already exists)."
    )
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {"name": {"type": "string", "description": "Client name."}},
        "required": ["name"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        client = await self._service.create_client(context.user_id, arguments["name"])
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps(_client_json(client))
        )


class UpdateClientTool(Tool):
    name = "workspace_update_client"
    description = (
        "Update a client's contact info or notes (email, phone, notes). Match the client by "
        "(partial) name. Only the fields you pass are changed."
    )
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "client_name": {"type": "string", "description": "Client name (or part of it)."},
            "email": {"type": "string", "description": "Contact email (optional)."},
            "phone": {"type": "string", "description": "Contact phone number (optional)."},
            "notes": {
                "type": "string",
                "description": "Free-text notes about the client (optional).",
            },
        },
        "required": ["client_name"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        client = await self._service.update_client(
            context.user_id,
            arguments["client_name"],
            email=arguments.get("email"),
            phone=arguments.get("phone"),
            notes=arguments.get("notes"),
        )
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps(_client_json(client))
        )


class GetClientDetailTool(Tool):
    name = "workspace_get_client_detail"
    description = (
        "Get a client's full history: contact info, notes, and every project and task linked "
        "to them. Match the client by (partial) name."
    )
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "client_name": {"type": "string", "description": "Client name (or part of it)."},
        },
        "required": ["client_name"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        detail = await self._service.get_client_detail(context.user_id, arguments["client_name"])
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps(_client_detail_json(detail))
        )


class CreateProjectTool(Tool):
    name = "workspace_create_project"
    description = (
        "Create a new project, optionally for a client (the client is created automatically "
        "if it doesn't exist yet)."
    )
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Project name."},
            "client_name": {
                "type": "string",
                "description": "Client this project is for (optional).",
            },
        },
        "required": ["name"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        project = await self._service.create_project(
            context.user_id, arguments["name"], arguments.get("client_name")
        )
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps(_project_json(project))
        )


class UpdateProjectStatusTool(Tool):
    name = "workspace_update_project_status"
    description = "Change a project's status. Match the project by (partial) name."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "project_name": {"type": "string", "description": "Project name (or part of it)."},
            "status": {
                "type": "string",
                "enum": [s.value for s in ProjectStatus],
                "description": "New status.",
            },
        },
        "required": ["project_name", "status"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        project = await self._service.update_project_status(
            context.user_id, arguments["project_name"], ProjectStatus(arguments["status"])
        )
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps(_project_json(project))
        )


class ListProjectsTool(Tool):
    name = "workspace_list_projects"
    description = "List the user's projects, most recently updated first."
    parameters_schema: dict[str, Any] = {"type": "object", "properties": {}, "required": []}
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        summaries = await self._service.list_projects(context.user_id)
        return ToolResult(
            tool_call_id="",
            tool_name=self.name,
            content=json.dumps([_project_summary_json(s) for s in summaries]),
        )


class CreateTaskTool(Tool):
    name = "workspace_create_task"
    description = "Create a new task, optionally under a project (matched by partial name)."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Task title."},
            "project_name": {
                "type": "string",
                "description": "Project this task belongs to (optional).",
            },
            "due_at": {
                "type": "string",
                "description": "Due date/time in ISO 8601 (optional), e.g. 2026-08-01T09:00:00Z.",
            },
        },
        "required": ["title"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        task = await self._service.create_task(
            context.user_id,
            arguments["title"],
            arguments.get("project_name"),
            _parse_due_at(arguments.get("due_at")),
        )
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps(_task_json(task))
        )


class UpdateTaskStatusTool(Tool):
    name = "workspace_update_task_status"
    description = "Change a task's status. Match the task by (partial) title."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "task_title": {"type": "string", "description": "Task title (or part of it)."},
            "status": {
                "type": "string",
                "enum": [s.value for s in TaskStatus],
                "description": "New status.",
            },
        },
        "required": ["task_title", "status"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        task = await self._service.update_task_status(
            context.user_id, arguments["task_title"], TaskStatus(arguments["status"])
        )
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps(_task_json(task))
        )


class SetTaskDueDateTool(Tool):
    name = "workspace_set_task_due_date"
    description = (
        "Set or clear a task's due date. Match the task by (partial) title. "
        "Omit due_at (or pass null) to clear the due date."
    )
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "task_title": {"type": "string", "description": "Task title (or part of it)."},
            "due_at": {
                "type": "string",
                "description": "Due date/time in ISO 8601, e.g. 2026-08-01T09:00:00Z.",
            },
        },
        "required": ["task_title"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        task = await self._service.set_task_due_at(
            context.user_id, arguments["task_title"], _parse_due_at(arguments.get("due_at"))
        )
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps(_task_json(task))
        )


class ListTasksTool(Tool):
    name = "workspace_list_tasks"
    description = "List the user's tasks, most recently updated first."
    parameters_schema: dict[str, Any] = {"type": "object", "properties": {}, "required": []}
    agent_name = AGENT_NAME

    def __init__(self, service: WorkspaceService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        tasks = await self._service.list_tasks(context.user_id)
        return ToolResult(
            tool_call_id="", tool_name=self.name, content=json.dumps([_task_json(t) for t in tasks])
        )
