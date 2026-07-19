from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import DriveFile


class DrivePort(ABC):
    """Read/write view of the user's Google Drive, for the dashboard files
    section — goes straight to the Drive API, bypassing the LLM tool-call
    loop (same reasoning as `InboxPort`/`SchedulePort`)."""

    @abstractmethod
    async def list_files(
        self, user_id: uuid.UUID, query: str | None, max_results: int
    ) -> list[DriveFile]:
        raise NotImplementedError

    @abstractmethod
    async def get_content(self, user_id: uuid.UUID, file_id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def create_file(
        self, user_id: uuid.UUID, name: str, content: str, mime_type: str
    ) -> DriveFile:
        raise NotImplementedError

    @abstractmethod
    async def share_file(self, user_id: uuid.UUID, file_id: str, email: str, role: str) -> None:
        raise NotImplementedError
