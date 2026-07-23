from __future__ import annotations

import uuid
from datetime import date

import pytest

from app.application.use_cases.finance_overview import FinanceOverviewUseCase
from app.core.exceptions import ExternalServiceError
from app.domain.entities import ExpenseRecord, IncomeRecord
from tests.conftest import FakeCache, FakeClientRepository, FakeGreenInvoicePort

USER_ID = uuid.uuid4()
FROM_DATE = date(2026, 7, 1)
TO_DATE = date(2026, 7, 31)


def _use_case() -> (
    tuple[FinanceOverviewUseCase, FakeGreenInvoicePort, FakeClientRepository, FakeCache]
):
    green_invoice = FakeGreenInvoicePort()
    clients = FakeClientRepository()
    cache = FakeCache()
    return FinanceOverviewUseCase(green_invoice, clients, cache), green_invoice, clients, cache


async def test_computes_totals_and_net() -> None:
    use_case, green_invoice, _clients, _cache = _use_case()
    green_invoice.income = [
        IncomeRecord(
            id="doc-1", date="2026-07-05", amount=1000.0, currency="ILS",
            client_name=None, description=None, status="OPENED_DOCUMENT",
        ),
        IncomeRecord(
            id="doc-2", date="2026-07-10", amount=500.0, currency="ILS",
            client_name=None, description=None, status="OPENED_DOCUMENT",
        ),
    ]
    green_invoice.expenses = [
        ExpenseRecord(id="exp-1", date="2026-07-06", amount=300.0, currency="ILS",
                      category=None, description=None),
    ]

    overview = await use_case.get_overview(USER_ID, FROM_DATE, TO_DATE)

    assert overview.total_income == 1500.0
    assert overview.total_expenses == 300.0
    assert overview.net == 1200.0


async def test_matches_income_to_existing_client_by_name_case_insensitive() -> None:
    use_case, green_invoice, clients, _cache = _use_case()
    client = await clients.create(USER_ID, "לקוח לדוגמה")
    green_invoice.income = [
        IncomeRecord(
            id="doc-1", date="2026-07-05", amount=1000.0, currency="ILS",
            client_name="לקוח לדוגמה".upper(), description=None, status="OPENED_DOCUMENT",
        ),
    ]

    overview = await use_case.get_overview(USER_ID, FROM_DATE, TO_DATE)

    assert overview.income[0].matched_client_id == client.id


async def test_unmatched_client_name_leaves_matched_client_id_none() -> None:
    use_case, green_invoice, clients, _cache = _use_case()
    await clients.create(USER_ID, "לקוח אחר")
    green_invoice.income = [
        IncomeRecord(
            id="doc-1", date="2026-07-05", amount=1000.0, currency="ILS",
            client_name="לקוח שלא קיים", description=None, status="OPENED_DOCUMENT",
        ),
    ]

    overview = await use_case.get_overview(USER_ID, FROM_DATE, TO_DATE)

    assert overview.income[0].matched_client_id is None


async def test_second_call_within_ttl_hits_cache_not_port() -> None:
    use_case, green_invoice, _clients, cache = _use_case()
    green_invoice.income = [
        IncomeRecord(id="doc-1", date="2026-07-05", amount=1000.0, currency="ILS",
                     client_name=None, description=None, status="OPENED_DOCUMENT"),
    ]

    first = await use_case.get_overview(USER_ID, FROM_DATE, TO_DATE)
    green_invoice._fail_with = ExternalServiceError  # a second live call would now raise
    second = await use_case.get_overview(USER_ID, FROM_DATE, TO_DATE)

    assert second.total_income == first.total_income == 1000.0
    assert len(cache.store) == 1


async def test_propagates_green_invoice_failure() -> None:
    use_case, green_invoice, _clients, _cache = _use_case()
    green_invoice._fail_with = ExternalServiceError

    with pytest.raises(ExternalServiceError):
        await use_case.get_overview(USER_ID, FROM_DATE, TO_DATE)
