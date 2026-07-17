from __future__ import annotations

import json
import uuid
from typing import Any

from app.agents.google_sheets.tools import (
    AppendRowTool,
    CreateSpreadsheetTool,
    ReadRangeTool,
    WriteRangeTool,
)
from app.application.ports.agent_tool import ToolExecutionContext


class _FakeSheetsClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def read_range(
        self, user_id: uuid.UUID, spreadsheet_id: str, cell_range: str
    ) -> list[list[str]]:
        self.calls.append(("read_range", (user_id, spreadsheet_id, cell_range)))
        return [["a", "b"], ["1", "2"]]

    async def write_range(
        self, user_id: uuid.UUID, spreadsheet_id: str, cell_range: str, values: list[list[str]]
    ) -> dict:
        self.calls.append(("write_range", (user_id, spreadsheet_id, cell_range, values)))
        return {"updatedCells": 4}

    async def append_row(
        self, user_id: uuid.UUID, spreadsheet_id: str, cell_range: str, values: list[str]
    ) -> dict:
        self.calls.append(("append_row", (user_id, spreadsheet_id, cell_range, values)))
        return {"updates": {"updatedRows": 1}}

    async def create_spreadsheet(self, user_id: uuid.UUID, title: str) -> dict:
        self.calls.append(("create_spreadsheet", (user_id, title)))
        return {"spreadsheetId": "sheet-1"}


def _context() -> ToolExecutionContext:
    return ToolExecutionContext(
        user_id=uuid.uuid4(), conversation_id=uuid.uuid4(), correlation_id="corr"
    )


async def test_read_range_tool() -> None:
    client = _FakeSheetsClient()
    tool = ReadRangeTool(client)
    context = _context()

    result = await tool.execute({"spreadsheet_id": "sheet-1", "range": "A1:B2"}, context)

    assert client.calls == [("read_range", (context.user_id, "sheet-1", "A1:B2"))]
    assert json.loads(result.content) == [["a", "b"], ["1", "2"]]


async def test_write_range_tool() -> None:
    client = _FakeSheetsClient()
    tool = WriteRangeTool(client)
    context = _context()

    await tool.execute(
        {"spreadsheet_id": "sheet-1", "range": "A1:B1", "values": [["x", "y"]]}, context
    )

    assert client.calls == [("write_range", (context.user_id, "sheet-1", "A1:B1", [["x", "y"]]))]


async def test_append_row_tool() -> None:
    client = _FakeSheetsClient()
    tool = AppendRowTool(client)
    context = _context()

    await tool.execute(
        {"spreadsheet_id": "sheet-1", "range": "A1", "values": ["a", "b"]}, context
    )

    assert client.calls == [("append_row", (context.user_id, "sheet-1", "A1", ["a", "b"]))]


async def test_create_spreadsheet_tool() -> None:
    client = _FakeSheetsClient()
    tool = CreateSpreadsheetTool(client)
    context = _context()

    result = await tool.execute({"title": "Budget 2026"}, context)

    assert client.calls == [("create_spreadsheet", (context.user_id, "Budget 2026"))]
    assert json.loads(result.content)["spreadsheetId"] == "sheet-1"
