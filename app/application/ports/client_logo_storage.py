from __future__ import annotations

import uuid
from abc import ABC, abstractmethod


class ClientLogoStoragePort(ABC):
    """Stores/retrieves client logo images and other per-client attachments in
    the user's own Google Drive — no separate storage infrastructure needed,
    and the bytes are only ever fetched server-side through an authenticated
    call, never exposed via a public link."""

    @abstractmethod
    async def upload(
        self, user_id: uuid.UUID, filename: str, content: bytes, mime_type: str
    ) -> str:
        """Uploads the file and returns its storage file id."""
        raise NotImplementedError

    @abstractmethod
    async def download(self, user_id: uuid.UUID, file_id: str) -> tuple[bytes, str]:
        """Returns (content, mime_type)."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, user_id: uuid.UUID, file_id: str) -> None:
        raise NotImplementedError
