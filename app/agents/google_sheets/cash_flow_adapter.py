"""Reads a small, dedicated `IDEA_OS` tab from the user's own cash-flow
Google Sheet — deliberately NOT an attempt to parse his full hand-formatted
planning sheet (whose column layout shifts between months). He adds a tab
with 4 label/value rows in any order; this adapter matches them by label
prefix and ignores everything else in the tab.
"""

from __future__ import annotations

import contextlib
import uuid
from datetime import UTC, datetime

from app.agents.google_sheets.client import SheetsClient
from app.application.ports.cash_flow_port import CashFlowPort
from app.domain.entities import CashFlowSnapshot

_TAB_RANGE = "IDEA_OS!A1:B10"

_LABEL_FIELDS = (
    ("יתרת עו\"ש נוכחית", "current_balance"),
    ("הוצאות קבועות החודש", "fixed_expenses_this_month"),
    ("חובה לרשויות החודש", "dues_this_month"),
    ("תחזית יתרה לסוף החודש", "projected_end_of_month_balance"),
)
_REQUIRED_FIELDS = frozenset(field for _, field in _LABEL_FIELDS)


class GoogleSheetsCashFlowAdapter(CashFlowPort):
    def __init__(self, client: SheetsClient, spreadsheet_id: str) -> None:
        self._client = client
        self._spreadsheet_id = spreadsheet_id

    async def get_snapshot(self, user_id: uuid.UUID) -> CashFlowSnapshot | None:
        if not self._spreadsheet_id:
            return None

        rows = await self._client.read_range(
            user_id, self._spreadsheet_id, _TAB_RANGE, value_render_option="UNFORMATTED_VALUE"
        )

        values: dict[str, float] = {}
        for row in rows:
            if len(row) < 2:
                continue
            label = str(row[0]).strip()
            for prefix, field in _LABEL_FIELDS:
                if label.startswith(prefix) and field not in values:
                    with contextlib.suppress(TypeError, ValueError):
                        values[field] = float(row[1])

        if not _REQUIRED_FIELDS.issubset(values):
            return None

        return CashFlowSnapshot(
            current_balance=values["current_balance"],
            fixed_expenses_this_month=values["fixed_expenses_this_month"],
            dues_this_month=values["dues_this_month"],
            projected_end_of_month_balance=values["projected_end_of_month_balance"],
            fetched_at=datetime.now(UTC),
        )
