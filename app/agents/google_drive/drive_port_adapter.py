from __future__ import annotations

import uuid
from typing import Any

from app.agents.google_drive.client import DriveClient
from app.application.ports.drive_port import DrivePort
from app.domain.entities import DriveFile


def _to_entity(raw: dict[str, Any]) -> DriveFile:
    return DriveFile(
        id=raw["id"],
        name=raw.get("name", ""),
        mime_type=raw.get("mimeType", ""),
        web_view_link=raw.get("webViewLink"),
        modified_time=raw.get("modifiedTime"),
    )


class GoogleDrivePortAdapter(DrivePort):
    def __init__(self, client: DriveClient) -> None:
        self._client = client

    async def list_files(
        self, user_id: uuid.UUID, query: str | None, max_results: int
    ) -> list[DriveFile]:
        files = await self._client.list_files(user_id, query, max_results)
        return [_to_entity(f) for f in files]

    async def get_content(self, user_id: uuid.UUID, file_id: str) -> str:
        return await self._client.get_file_content(user_id, file_id)

    async def create_file(
        self, user_id: uuid.UUID, name: str, content: str, mime_type: str
    ) -> DriveFile:
        file = await self._client.create_file(user_id, name, content, mime_type)
        return _to_entity(file)

    async def share_file(self, user_id: uuid.UUID, file_id: str, email: str, role: str) -> None:
        await self._client.share_file(user_id, file_id, email, role)
