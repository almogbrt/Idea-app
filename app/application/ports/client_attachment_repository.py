from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import ClientAttachment


class ClientAttachmentRepositoryPort(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: uuid.UUID,
        client_id: uuid.UUID,
        file_id: str,
        filename: str,
        mime_type: str,
    ) -> ClientAttachment:
        raise NotImplementedError

    @abstractmethod
    async def list_by_client(self, client_id: uuid.UUID) -> list[ClientAttachment]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, attachment_id: uuid.UUID) -> ClientAttachment | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, attachment_id: uuid.UUID) -> None:
        raise NotImplementedError
