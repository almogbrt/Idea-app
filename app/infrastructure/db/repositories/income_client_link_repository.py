from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.income_client_link_repository import IncomeClientLinkRepositoryPort
from app.infrastructure.db.models import IncomeClientLinkModel


class SqlAlchemyIncomeClientLinkRepository(IncomeClientLinkRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_all(self, user_id: uuid.UUID) -> dict[str, uuid.UUID]:
        rows = (
            await self._session.scalars(
                select(IncomeClientLinkModel).where(IncomeClientLinkModel.user_id == user_id)
            )
        ).all()
        return {row.green_invoice_client_id: row.client_id for row in rows}

    async def upsert(
        self,
        user_id: uuid.UUID,
        green_invoice_client_id: str,
        green_invoice_client_name: str,
        client_id: uuid.UUID,
    ) -> None:
        stmt = (
            insert(IncomeClientLinkModel)
            .values(
                user_id=user_id,
                green_invoice_client_id=green_invoice_client_id,
                green_invoice_client_name=green_invoice_client_name,
                client_id=client_id,
            )
            .on_conflict_do_update(
                index_elements=[
                    IncomeClientLinkModel.user_id,
                    IncomeClientLinkModel.green_invoice_client_id,
                ],
                set_={
                    "green_invoice_client_name": green_invoice_client_name,
                    "client_id": client_id,
                },
            )
        )
        await self._session.execute(stmt)
        await self._session.flush()
