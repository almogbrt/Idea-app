from __future__ import annotations

import uuid

from app.application.ports.drive_port import DrivePort
from app.domain.entities import DriveFile


class ManageFilesUseCase:
    def __init__(self, drive: DrivePort) -> None:
        self._drive = drive

    async def list_files(
        self, user_id: uuid.UUID, query: str | None = None, max_results: int = 50
    ) -> list[DriveFile]:
        return await self._drive.list_files(user_id, query, max_results)

    async def get_content(self, user_id: uuid.UUID, file_id: str) -> str:
        return await self._drive.get_content(user_id, file_id)

    async def create_file(
        self, user_id: uuid.UUID, name: str, content: str, mime_type: str = "text/plain"
    ) -> DriveFile:
        return await self._drive.create_file(user_id, name, content, mime_type)

    async def share_file(
        self, user_id: uuid.UUID, file_id: str, email: str, role: str = "reader"
    ) -> None:
        await self._drive.share_file(user_id, file_id, email, role)
