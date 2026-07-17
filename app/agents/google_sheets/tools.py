from __future__ import annotations

import json
from typing import Any

from app.agents.google_sheets.client import SheetsClient
from app.application.ports.agent_tool import Tool, ToolExecutionContext
from app.domain.entities import ToolResult

AGENT_NAME = "google_sheets"


class ReadRangeTool(Tool):
    name = "sheets_read_range"
    description = "Read cell values from a range in a Google Sheet (e.g. 'Sheet1!A1:D20')."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "spreadsheet_id": {"type": "string", "description": "Google Sheets spreadsheet ID."},
            "range": {"type": "string", "description": "A1-notation range, e.g. 'Sheet1!A1:D20'."},
        },
        "required": ["spreadsheet_id", "range"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: SheetsClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        values = await self._client.read_range(
            context.user_id, arguments["spreadsheet_id"], arguments["range"]
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(values))


class WriteRangeTool(Tool):
    name = "sheets_write_range"
    description = "Overwrite cell values in a range of a Google Sheet."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "spreadsheet_id": {"type": "string", "description": "Google Sheets spreadsheet ID."},
            "range": {"type": "string", "description": "A1-notation range, e.g. 'Sheet1!A1:D20'."},
            "values": {
                "type": "array",
                "items": {"type": "array", "items": {"type": "string"}},
                "description": "2D array of row values to write.",
            },
        },
        "required": ["spreadsheet_id", "range", "values"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: SheetsClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        result = await self._client.write_range(
            context.user_id, arguments["spreadsheet_id"], arguments["range"], arguments["values"]
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(result))


class AppendRowTool(Tool):
    name = "sheets_append_row"
    description = "Append a single row to the end of a table in a Google Sheet."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "spreadsheet_id": {"type": "string", "description": "Google Sheets spreadsheet ID."},
            "range": {"type": "string", "description": "A1-notation range identifying the table."},
            "values": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Row values to append.",
            },
        },
        "required": ["spreadsheet_id", "range", "values"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: SheetsClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        result = await self._client.append_row(
            context.user_id, arguments["spreadsheet_id"], arguments["range"], arguments["values"]
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(result))


class CreateSpreadsheetTool(Tool):
    name = "sheets_create_spreadsheet"
    description = "Create a brand new Google Sheets spreadsheet with the given title."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {"title": {"type": "string", "description": "Spreadsheet title."}},
        "required": ["title"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: SheetsClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        result = await self._client.create_spreadsheet(context.user_id, arguments["title"])
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(result))
