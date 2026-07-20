from __future__ import annotations

import json
from typing import Any

from app.agents.google_drive.client import DriveClient
from app.application.ports.agent_tool import Tool, ToolExecutionContext
from app.domain.entities import ToolResult

AGENT_NAME = "google_drive"


class ListFilesTool(Tool):
    name = "drive_list_files"
    description = (
        "List or search files in the user's Google Drive. `query` accepts native Drive "
        "search syntax (e.g. \"name contains 'invoice'\" or "
        "\"mimeType='application/vnd.google-apps.spreadsheet'\"). "
        "Omit `query` to list the most recently modified files."
    )
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Drive API search query (optional)."},
            "max_results": {
                "type": "integer",
                "description": "Maximum number of files to return.",
                "default": 10,
            },
        },
        "required": [],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: DriveClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        files = await self._client.list_files(
            context.user_id, arguments.get("query"), arguments.get("max_results", 10)
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(files))


class GetFileContentTool(Tool):
    name = "drive_get_file_content"
    description = "Read the text content of a file in Google Drive by its file ID."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {"file_id": {"type": "string", "description": "Google Drive file ID."}},
        "required": ["file_id"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: DriveClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        content = await self._client.get_file_content(context.user_id, arguments["file_id"])
        return ToolResult(tool_call_id="", tool_name=self.name, content=content)


class CreateFileTool(Tool):
    name = "drive_create_file"
    description = (
        "Create a new file in the user's Google Drive with the given text content. "
        "Set as_google_doc=true when the user asks for a Word/Google Doc-style document "
        "rather than a plain text file. Set folder_name to place the file inside a "
        "specific Drive folder — the folder is created automatically if it doesn't "
        "already exist."
    )
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "File name."},
            "content": {"type": "string", "description": "Text content of the file."},
            "mime_type": {
                "type": "string",
                "description": "MIME type of the file.",
                "default": "text/plain",
            },
            "as_google_doc": {
                "type": "boolean",
                "description": (
                    "Create the file as a native Google Doc (opens as a Word-style "
                    "document) instead of a plain file."
                ),
                "default": False,
            },
            "folder_name": {
                "type": "string",
                "description": (
                    "Name of the Drive folder to create the file in. Created "
                    "automatically if no folder with this name exists yet."
                ),
            },
        },
        "required": ["name", "content"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: DriveClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        parent_folder_id = None
        folder_name = arguments.get("folder_name")
        if folder_name:
            parent_folder_id = await self._client.find_folder_by_name(
                context.user_id, folder_name
            )
            if parent_folder_id is None:
                parent_folder_id = await self._client.create_folder(context.user_id, folder_name)

        target_mime_type = (
            "application/vnd.google-apps.document" if arguments.get("as_google_doc") else None
        )
        result = await self._client.create_file(
            context.user_id,
            arguments["name"],
            arguments["content"],
            arguments.get("mime_type", "text/plain"),
            parent_folder_id=parent_folder_id,
            target_mime_type=target_mime_type,
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(result))


class ShareFileTool(Tool):
    name = "drive_share_file"
    description = "Share a Google Drive file with another person's email address."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "file_id": {"type": "string", "description": "Google Drive file ID."},
            "email": {"type": "string", "description": "Email address to share with."},
            "role": {
                "type": "string",
                "description": "Access role to grant.",
                "enum": ["reader", "commenter", "writer"],
                "default": "reader",
            },
        },
        "required": ["file_id", "email"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: DriveClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        result = await self._client.share_file(
            context.user_id,
            arguments["file_id"],
            arguments["email"],
            arguments.get("role", "reader"),
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(result))
