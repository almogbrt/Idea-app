from __future__ import annotations

import uuid
from abc import ABC, abstractmethod


class ClientLogoStoragePort(ABC):
    """Stores/retrieves client logo images in the user's own Google Drive —
    no separate storage infrastructure needed, and the image bytes are only
    ever fetched server-side through an authenticated call, never exposed
    via a public link."""

    @abstractmethod
    async def upload(
        self, user_id: uuid.UUID, filename: str, content: bytes, mime_type: str
    ) -> str:
        """Uploads the logo image and returns its storage file id."""
        raise NotImplementedError

    @abstractmethod
    async def download(self, user_id: uuid.UUID, file_id: str) -> tuple[bytes, str]:
        """Returns (content, mime_type)."""
        raise NotImplementedError
