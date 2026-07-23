from __future__ import annotations

import uuid
from typing import Any

from app.agents.google_sheets.cash_flow_adapter import GoogleSheetsCashFlowAdapter

USER_ID = uuid.uuid4()
SPREADSHEET_ID = "sheet-123"


class _FakeSheetsClient:
    def __init__(self, rows: list[list[Any]]) -> None:
        self._rows = rows
        self.calls: list[tuple[uuid.UUID, str, str, str]] = []

    async def read_range(
        self,
        user_id: uuid.UUID,
        spreadsheet_id: str,
        cell_range: str,
        value_render_option: str = "FORMATTED_VALUE",
    ) -> list[list[Any]]:
        self.calls.append((user_id, spreadsheet_id, cell_range, value_render_option))
        return self._rows


_HAPPY_ROWS: list[list[Any]] = [
    ['יתרת עו"ש נוכחית', -23622],
    ["הוצאות קבועות החודש", -2510],
    ["חובה לרשויות החודש (מס+ביטוח לאומי+פנסיה)", -4617.46],
    ["תחזית יתרה לסוף החודש", -30201],
]


async def test_happy_path_all_labels_present_in_any_order() -> None:
    shuffled = list(reversed(_HAPPY_ROWS))
    client = _FakeSheetsClient(shuffled)
    adapter = GoogleSheetsCashFlowAdapter(client, SPREADSHEET_ID)

    snapshot = await adapter.get_snapshot(USER_ID)

    assert snapshot is not None
    assert snapshot.current_balance == -23622
    assert snapshot.fixed_expenses_this_month == -2510
    assert snapshot.dues_this_month == -4617.46
    assert snapshot.projected_end_of_month_balance == -30201
    assert client.calls[0][3] == "UNFORMATTED_VALUE"


async def test_missing_spreadsheet_id_returns_none_without_calling_client() -> None:
    client = _FakeSheetsClient(_HAPPY_ROWS)
    adapter = GoogleSheetsCashFlowAdapter(client, "")

    snapshot = await adapter.get_snapshot(USER_ID)

    assert snapshot is None
    assert client.calls == []


async def test_missing_label_returns_none() -> None:
    incomplete = _HAPPY_ROWS[:3]
    client = _FakeSheetsClient(incomplete)
    adapter = GoogleSheetsCashFlowAdapter(client, SPREADSHEET_ID)

    snapshot = await adapter.get_snapshot(USER_ID)

    assert snapshot is None


async def test_ignores_unrelated_rows_and_blank_rows() -> None:
    rows_with_noise: list[list[Any]] = [
        [],
        ["הערה כלשהי"],
        *_HAPPY_ROWS,
        ["שורה נוספת לא רלוונטית", 999],
    ]
    client = _FakeSheetsClient(rows_with_noise)
    adapter = GoogleSheetsCashFlowAdapter(client, SPREADSHEET_ID)

    snapshot = await adapter.get_snapshot(USER_ID)

    assert snapshot is not None
    assert snapshot.current_balance == -23622


async def test_label_prefix_tolerates_trailing_note() -> None:
    client = _FakeSheetsClient(_HAPPY_ROWS)
    adapter = GoogleSheetsCashFlowAdapter(client, SPREADSHEET_ID)

    snapshot = await adapter.get_snapshot(USER_ID)

    assert snapshot is not None
    assert snapshot.dues_this_month == -4617.46
