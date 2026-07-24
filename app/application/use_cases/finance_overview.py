"""Dashboard finance section: aggregates Green Invoice income/expense data
and links income records to existing IDEA OS clients, purely for display —
never writes anything back to Green Invoice or to the local database."""

from __future__ import annotations

import json
import uuid
from dataclasses import replace
from datetime import UTC, date, datetime

from app.application.ports.cache import CachePort
from app.application.ports.client_repository import ClientRepositoryPort
from app.application.ports.green_invoice_port import GreenInvoicePort
from app.application.ports.income_client_link_repository import IncomeClientLinkRepositoryPort
from app.domain.entities import ExpenseRecord, FinanceOverview, IncomeRecord

_CACHE_TTL_SECONDS = 300
"""Green Invoice's rate limit is ~3 req/s; a 5-minute cache keeps repeated
dashboard loads cheap without needing a standing sync job."""


class FinanceOverviewUseCase:
    def __init__(
        self,
        green_invoice_port: GreenInvoicePort,
        client_repository: ClientRepositoryPort,
        cache: CachePort,
        income_client_links: IncomeClientLinkRepositoryPort,
    ) -> None:
        self._green_invoice = green_invoice_port
        self._clients = client_repository
        self._cache = cache
        self._income_client_links = income_client_links

    async def get_overview(
        self, user_id: uuid.UUID, from_date: date, to_date: date
    ) -> FinanceOverview:
        cache_key = (
            f"green-invoice:overview:{user_id}:{from_date.isoformat()}:{to_date.isoformat()}"
        )
        cached = await self._cache.get(cache_key)
        if cached is not None:
            return _deserialize(cached)

        income = await self._green_invoice.list_income(from_date, to_date)
        expenses = await self._green_invoice.list_expenses(from_date, to_date)
        matched_income = await self._match_clients(user_id, income)
        total_income = sum(record.amount for record in matched_income)
        total_expenses = sum(record.amount for record in expenses)
        overview = FinanceOverview(
            from_date=from_date,
            to_date=to_date,
            income=matched_income,
            expenses=expenses,
            total_income=total_income,
            total_expenses=total_expenses,
            net=total_income - total_expenses,
        )

        await self._cache.set(cache_key, _serialize(overview), ttl_seconds=_CACHE_TTL_SECONDS)
        return overview

    async def link_income_client(
        self,
        user_id: uuid.UUID,
        green_invoice_client_id: str,
        green_invoice_client_name: str,
        client_id: uuid.UUID,
    ) -> None:
        await self._income_client_links.upsert(
            user_id, green_invoice_client_id, green_invoice_client_name, client_id
        )
        # Invalidate the default "this month to today" cache entry so the
        # new link is reflected immediately, not after a 5-minute wait —
        # this is the only date range the dashboard ever actually requests.
        today = datetime.now(UTC).date()
        cache_key = (
            f"green-invoice:overview:{user_id}:"
            f"{today.replace(day=1).isoformat()}:{today.isoformat()}"
        )
        await self._cache.delete(cache_key)

    async def _match_clients(
        self, user_id: uuid.UUID, income: list[IncomeRecord]
    ) -> list[IncomeRecord]:
        clients = await self._clients.list_by_user(user_id)
        by_name = {client.name.strip().lower(): client.id for client in clients}
        manual_links = await self._income_client_links.get_all(user_id)

        def _match(record: IncomeRecord) -> IncomeRecord:
            manual_match = (
                manual_links.get(record.green_invoice_client_id)
                if record.green_invoice_client_id
                else None
            )
            if manual_match is not None:
                return replace(record, matched_client_id=manual_match)
            if record.client_name:
                return replace(
                    record, matched_client_id=by_name.get(record.client_name.strip().lower())
                )
            return record

        return [_match(record) for record in income]


def _serialize(overview: FinanceOverview) -> str:
    return json.dumps(
        {
            "from_date": overview.from_date.isoformat(),
            "to_date": overview.to_date.isoformat(),
            "income": [
                {
                    "id": r.id,
                    "date": r.date,
                    "amount": r.amount,
                    "currency": r.currency,
                    "client_name": r.client_name,
                    "description": r.description,
                    "status": r.status,
                    "green_invoice_client_id": r.green_invoice_client_id,
                    "matched_client_id": str(r.matched_client_id) if r.matched_client_id else None,
                }
                for r in overview.income
            ],
            "expenses": [
                {
                    "id": r.id,
                    "date": r.date,
                    "amount": r.amount,
                    "currency": r.currency,
                    "category": r.category,
                    "description": r.description,
                }
                for r in overview.expenses
            ],
            "total_income": overview.total_income,
            "total_expenses": overview.total_expenses,
            "net": overview.net,
        }
    )


def _deserialize(raw: str) -> FinanceOverview:
    data = json.loads(raw)
    return FinanceOverview(
        from_date=date.fromisoformat(data["from_date"]),
        to_date=date.fromisoformat(data["to_date"]),
        income=[
            IncomeRecord(
                id=item["id"],
                date=item["date"],
                amount=item["amount"],
                currency=item["currency"],
                client_name=item["client_name"],
                description=item["description"],
                status=item["status"],
                green_invoice_client_id=item.get("green_invoice_client_id"),
                matched_client_id=(
                    uuid.UUID(item["matched_client_id"]) if item["matched_client_id"] else None
                ),
            )
            for item in data["income"]
        ],
        expenses=[
            ExpenseRecord(
                id=item["id"],
                date=item["date"],
                amount=item["amount"],
                currency=item["currency"],
                category=item["category"],
                description=item["description"],
            )
            for item in data["expenses"]
        ],
        total_income=data["total_income"],
        total_expenses=data["total_expenses"],
        net=data["net"],
    )
