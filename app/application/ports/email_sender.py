from __future__ import annotations

import uuid
from abc import ABC, abstractmethod


class EmailSenderPort(ABC):
    """Narrow write-only view for sending a single email, for background jobs
    (reminders) that need to notify the owner without going through the LLM
    tool-call loop."""

    @abstractmethod
    async def send(self, user_id: uuid.UUID, to: str, subject: str, body: str) -> None:
        raise NotImplementedError
