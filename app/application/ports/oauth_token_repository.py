from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.value_objects import OAuthTokenSet


class OAuthTokenRepositoryPort(ABC):
    @abstractmethod
    async def save_tokens(
        self, user_id: uuid.UUID, provider: str, tokens: OAuthTokenSet
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_tokens(self, user_id: uuid.UUID, provider: str) -> OAuthTokenSet | None:
        raise NotImplementedError
