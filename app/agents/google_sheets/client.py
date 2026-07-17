"""Thin wrapper around the Google Sheets v4 API for this agent's needs."""

from __future__ import annotations

import uuid
from typing import Any, cast

from app.agents._shared import call_google_api
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory


class SheetsClient:
    def __init__(self, google_clients: GoogleApiClientFactory) -> None:
        self._google_clients = google_clients

    async def read_range(
        self, user_id: uuid.UUID, spreadsheet_id: str, cell_range: str
    ) -> list[list[str]]:
        service = await self._google_clients.sheets(user_id)
        response = await call_google_api(
            lambda: service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=cell_range)
            .execute(),
            action="sheets.values.get",
        )
        return cast(list[list[str]], response.get("values", []))

    async def write_range(
        self, user_id: uuid.UUID, spreadsheet_id: str, cell_range: str, values: list[list[str]]
    ) -> dict[str, Any]:
        service = await self._google_clients.sheets(user_id)
        return await call_google_api(
            lambda: service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=cell_range,
                valueInputOption="USER_ENTERED",
                body={"values": values},
            )
            .execute(),
            action="sheets.values.update",
        )

    async def append_row(
        self, user_id: uuid.UUID, spreadsheet_id: str, cell_range: str, values: list[str]
    ) -> dict[str, Any]:
        service = await self._google_clients.sheets(user_id)
        return await call_google_api(
            lambda: service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=cell_range,
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body={"values": [values]},
            )
            .execute(),
            action="sheets.values.append",
        )

    async def create_spreadsheet(self, user_id: uuid.UUID, title: str) -> dict[str, Any]:
        service = await self._google_clients.sheets(user_id)
        return await call_google_api(
            lambda: service.spreadsheets()
            .create(body={"properties": {"title": title}}, fields="spreadsheetId,spreadsheetUrl")
            .execute(),
            action="sheets.spreadsheets.create",
        )
