from __future__ import annotations

import json
import uuid
from typing import Any

from app.agents.google_drive.tools import (
    CreateFileTool,
    GetFileContentTool,
    ListFilesTool,
    ShareFileTool,
)
from app.application.ports.agent_tool import ToolExecutionContext


class _FakeDriveClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []
        self.existing_folders: dict[str, str] = {}

    async def list_files(
        self, user_id: uuid.UUID, query: str | None, max_results: int
    ) -> list[dict]:
        self.calls.append(("list_files", (user_id, query, max_results)))
        return [{"id": "file-1", "name": "Q3 Report.pdf"}]

    async def get_file_content(self, user_id: uuid.UUID, file_id: str) -> str:
        self.calls.append(("get_file_content", (user_id, file_id)))
        return "file contents here"

    async def create_file(
        self,
        user_id: uuid.UUID,
        name: str,
        content: str,
        mime_type: str,
        parent_folder_id: str | None = None,
        target_mime_type: str | None = None,
    ) -> dict:
        self.calls.append(
            (
                "create_file",
                (user_id, name, content, mime_type, parent_folder_id, target_mime_type),
            )
        )
        return {"id": "new-file", "name": name}

    async def find_folder_by_name(self, user_id: uuid.UUID, name: str) -> str | None:
        self.calls.append(("find_folder_by_name", (user_id, name)))
        return self.existing_folders.get(name)

    async def create_folder(self, user_id: uuid.UUID, name: str) -> str:
        self.calls.append(("create_folder", (user_id, name)))
        return "new-folder-id"

    async def share_file(self, user_id: uuid.UUID, file_id: str, email: str, role: str) -> dict:
        self.calls.append(("share_file", (user_id, file_id, email, role)))
        return {"id": "permission-1"}


def _context() -> ToolExecutionContext:
    return ToolExecutionContext(
        user_id=uuid.uuid4(), conversation_id=uuid.uuid4(), correlation_id="corr"
    )


async def test_list_files_tool_delegates_and_serializes() -> None:
    client = _FakeDriveClient()
    tool = ListFilesTool(client)
    context = _context()

    result = await tool.execute({"query": "invoice", "max_results": 5}, context)

    assert client.calls == [("list_files", (context.user_id, "invoice", 5))]
    assert json.loads(result.content) == [{"id": "file-1", "name": "Q3 Report.pdf"}]
    assert result.is_error is False


async def test_list_files_tool_defaults_max_results() -> None:
    client = _FakeDriveClient()
    tool = ListFilesTool(client)
    context = _context()

    await tool.execute({}, context)

    assert client.calls == [("list_files", (context.user_id, None, 10))]


async def test_get_file_content_tool_returns_raw_text() -> None:
    client = _FakeDriveClient()
    tool = GetFileContentTool(client)
    context = _context()

    result = await tool.execute({"file_id": "file-1"}, context)

    assert result.content == "file contents here"


async def test_create_file_tool_defaults_mime_type() -> None:
    client = _FakeDriveClient()
    tool = CreateFileTool(client)
    context = _context()

    await tool.execute({"name": "notes.txt", "content": "hello"}, context)

    assert client.calls == [
        ("create_file", (context.user_id, "notes.txt", "hello", "text/plain", None, None))
    ]


async def test_create_file_tool_as_google_doc_sets_target_mime_type() -> None:
    client = _FakeDriveClient()
    tool = CreateFileTool(client)
    context = _context()

    await tool.execute(
        {"name": "Proposal", "content": "hello", "as_google_doc": True}, context
    )

    assert client.calls == [
        (
            "create_file",
            (
                context.user_id,
                "Proposal",
                "hello",
                "text/plain",
                None,
                "application/vnd.google-apps.document",
            ),
        )
    ]


async def test_create_file_tool_reuses_existing_folder() -> None:
    client = _FakeDriveClient()
    client.existing_folders["Contracts"] = "folder-123"
    tool = CreateFileTool(client)
    context = _context()

    await tool.execute(
        {"name": "notes.txt", "content": "hello", "folder_name": "Contracts"}, context
    )

    assert client.calls == [
        ("find_folder_by_name", (context.user_id, "Contracts")),
        ("create_file", (context.user_id, "notes.txt", "hello", "text/plain", "folder-123", None)),
    ]


async def test_create_file_tool_creates_missing_folder() -> None:
    client = _FakeDriveClient()
    tool = CreateFileTool(client)
    context = _context()

    await tool.execute(
        {"name": "notes.txt", "content": "hello", "folder_name": "New Folder"}, context
    )

    assert client.calls == [
        ("find_folder_by_name", (context.user_id, "New Folder")),
        ("create_folder", (context.user_id, "New Folder")),
        (
            "create_file",
            (context.user_id, "notes.txt", "hello", "text/plain", "new-folder-id", None),
        ),
    ]


async def test_share_file_tool_defaults_role_to_reader() -> None:
    client = _FakeDriveClient()
    tool = ShareFileTool(client)
    context = _context()

    await tool.execute({"file_id": "file-1", "email": "someone@example.com"}, context)

    assert client.calls == [
        ("share_file", (context.user_id, "file-1", "someone@example.com", "reader"))
    ]


def test_tool_definitions_expose_valid_json_schema() -> None:
    client = _FakeDriveClient()
    for tool in [ListFilesTool(client), GetFileContentTool(client), CreateFileTool(client)]:
        definition = tool.definition()
        assert definition.name == tool.name
        assert definition.parameters_schema["type"] == "object"
        assert definition.agent_name == "google_drive"
