from __future__ import annotations

import uuid
from abc import ABC, abstractmethod


class IncomeClientLinkRepositoryPort(ABC):
    """Manual overrides mapping a Green Invoice client id to an IDEA OS
    client, for income records that don't auto-match by name."""

    @abstractmethod
    async def get_all(self, user_id: uuid.UUID) -> dict[str, uuid.UUID]:
        """Returns green_invoice_client_id -> client_id for this user."""
        raise NotImplementedError

    @abstractmethod
    async def upsert(
        self,
        user_id: uuid.UUID,
        green_invoice_client_id: str,
        green_invoice_client_name: str,
        client_id: uuid.UUID,
    ) -> None:
        raise NotImplementedError
