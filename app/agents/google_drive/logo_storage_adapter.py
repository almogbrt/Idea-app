from __future__ import annotations

import uuid

from app.agents.google_drive.client import DriveClient
from app.application.ports.client_logo_storage import ClientLogoStoragePort


class GoogleDriveLogoStorageAdapter(ClientLogoStoragePort):
    def __init__(self, client: DriveClient) -> None:
        self._client = client

    async def upload(
        self, user_id: uuid.UUID, filename: str, content: bytes, mime_type: str
    ) -> str:
        file = await self._client.upload_binary_file(user_id, filename, content, mime_type)
        return str(file["id"])

    async def download(self, user_id: uuid.UUID, file_id: str) -> tuple[bytes, str]:
        return await self._client.download_binary_file(user_id, file_id)
