from __future__ import annotations

import time
from datetime import date, timedelta

import jwt
import pytest
import respx
from httpx import Response

from app.core.exceptions import AuthError, ExternalServiceError
from app.infrastructure.green_invoice.client import GreenInvoiceClient

_BASE_URL = "https://api.greeninvoice.co.il/api/v1"


def _make_token(expires_in_seconds: int) -> str:
    payload = {"exp": int(time.time()) + expires_in_seconds}
    return jwt.encode(payload, "irrelevant-signing-key", algorithm="HS256")


@respx.mock
async def test_list_income_authenticates_then_fetches_and_parses() -> None:
    token = _make_token(1800)
    respx.post(f"{_BASE_URL}/account/token").mock(
        return_value=Response(200, json={"token": token})
    )
    respx.post(f"{_BASE_URL}/documents/search").mock(
        return_value=Response(
            200,
            json={
                "items": [
                    {
                        "id": "doc-1",
                        "date": "2026-07-01",
                        "amount": 1500.5,
                        "currency": "ILS",
                        "client": {"id": "c-1", "name": "לקוח לדוגמה"},
                        "remarks": "ייעוץ יולי",
                        "status": "OPENED_DOCUMENT",
                    }
                ]
            },
        )
    )
    client = GreenInvoiceClient("api-id", "api-secret", _BASE_URL)

    records = await client.list_income(date(2026, 7, 1), date(2026, 7, 31))

    assert len(records) == 1
    record = records[0]
    assert record.id == "doc-1"
    assert record.amount == 1500.5
    assert record.currency == "ILS"
    assert record.client_name == "לקוח לדוגמה"
    assert record.description == "ייעוץ יולי"
    assert record.status == "OPENED_DOCUMENT"


@respx.mock
async def test_list_income_excludes_quotes_and_orders() -> None:
    """`/documents/search` returns every document type in range, including
    price quotes and orders that were never actually paid — these must not
    be counted as income."""
    respx.post(f"{_BASE_URL}/account/token").mock(
        return_value=Response(200, json={"token": _make_token(1800)})
    )
    respx.post(f"{_BASE_URL}/documents/search").mock(
        return_value=Response(
            200,
            json={
                "items": [
                    {"id": "quote-1", "type": 10, "amount": 5000, "date": "2026-07-01"},
                    {"id": "order-1", "type": 100, "amount": 3000, "date": "2026-07-02"},
                    {"id": "invoice-1", "type": 320, "amount": 1000, "date": "2026-07-03"},
                ]
            },
        )
    )
    client = GreenInvoiceClient("api-id", "api-secret", _BASE_URL)

    records = await client.list_income(date(2026, 7, 1), date(2026, 7, 31))

    assert [r.id for r in records] == ["invoice-1"]


@respx.mock
async def test_list_income_excludes_transaction_account_shadow_of_a_real_sale() -> None:
    """Green Invoice auto-generates a type-300 "Transaction Account" entry
    alongside every real sale document (e.g. type 320), carrying the same
    amount as an internal accounting-ledger mirror — not a second sale."""
    respx.post(f"{_BASE_URL}/account/token").mock(
        return_value=Response(200, json={"token": _make_token(1800)})
    )
    respx.post(f"{_BASE_URL}/documents/search").mock(
        return_value=Response(
            200,
            json={
                "items": [
                    {"id": "invoice-1", "type": 320, "amount": 8850},
                    {"id": "ledger-shadow-1", "type": 300, "amount": 8850},
                ]
            },
        )
    )
    client = GreenInvoiceClient("api-id", "api-secret", _BASE_URL)

    records = await client.list_income(date(2026, 7, 1), date(2026, 7, 31))

    assert [r.id for r in records] == ["invoice-1"]


@respx.mock
async def test_list_income_treats_credit_invoice_as_negative() -> None:
    respx.post(f"{_BASE_URL}/account/token").mock(
        return_value=Response(200, json={"token": _make_token(1800)})
    )
    respx.post(f"{_BASE_URL}/documents/search").mock(
        return_value=Response(
            200,
            json={"items": [{"id": "credit-1", "type": 330, "amount": 200, "date": "2026-07-05"}]},
        )
    )
    client = GreenInvoiceClient("api-id", "api-secret", _BASE_URL)

    records = await client.list_income(date(2026, 7, 1), date(2026, 7, 31))

    assert records[0].amount == -200.0


@respx.mock
async def test_list_expenses_parses_defensively_with_missing_fields() -> None:
    respx.post(f"{_BASE_URL}/account/token").mock(
        return_value=Response(200, json={"token": _make_token(1800)})
    )
    respx.post(f"{_BASE_URL}/expenses/search").mock(
        return_value=Response(200, json={"items": [{"id": "exp-1", "price": 200}]})
    )
    client = GreenInvoiceClient("api-id", "api-secret", _BASE_URL)

    records = await client.list_expenses(date(2026, 7, 1), date(2026, 7, 31))

    assert records[0].id == "exp-1"
    assert records[0].amount == 200.0
    assert records[0].currency == "ILS"
    assert records[0].category is None


@respx.mock
async def test_reuses_cached_token_across_calls() -> None:
    token_route = respx.post(f"{_BASE_URL}/account/token").mock(
        return_value=Response(200, json={"token": _make_token(1800)})
    )
    respx.post(f"{_BASE_URL}/documents/search").mock(return_value=Response(200, json={"items": []}))
    client = GreenInvoiceClient("api-id", "api-secret", _BASE_URL)

    await client.list_income(date(2026, 7, 1), date(2026, 7, 31))
    await client.list_income(date(2026, 8, 1), date(2026, 8, 31))

    assert token_route.call_count == 1


@respx.mock
async def test_refetches_token_once_expired() -> None:
    token_route = respx.post(f"{_BASE_URL}/account/token").mock(
        side_effect=[
            Response(200, json={"token": _make_token(-5)}),
            Response(200, json={"token": _make_token(1800)}),
        ]
    )
    respx.post(f"{_BASE_URL}/documents/search").mock(return_value=Response(200, json={"items": []}))
    client = GreenInvoiceClient("api-id", "api-secret", _BASE_URL)

    await client.list_income(date(2026, 7, 1), date(2026, 7, 31))
    await client.list_income(date(2026, 8, 1), date(2026, 8, 31))

    assert token_route.call_count == 2


@respx.mock
async def test_invalid_credentials_raise_auth_error() -> None:
    respx.post(f"{_BASE_URL}/account/token").mock(
        return_value=Response(401, json={"message": "invalid credentials"})
    )
    client = GreenInvoiceClient("bad-id", "bad-secret", _BASE_URL)

    with pytest.raises(AuthError):
        await client.list_income(date(2026, 7, 1), date(2026, 7, 31))


@respx.mock
async def test_downstream_5xx_raises_external_service_error() -> None:
    respx.post(f"{_BASE_URL}/account/token").mock(
        return_value=Response(200, json={"token": _make_token(1800)})
    )
    respx.post(f"{_BASE_URL}/documents/search").mock(return_value=Response(503, text="down"))
    client = GreenInvoiceClient("api-id", "api-secret", _BASE_URL)

    with pytest.raises(ExternalServiceError):
        await client.list_income(date(2026, 7, 1), date(2026, 7, 31))


def test_token_expiry_falls_back_when_claim_missing() -> None:
    from app.infrastructure.green_invoice.client import _token_expiry

    before = time.time()
    expiry = _token_expiry("not-a-real-jwt")
    assert expiry > before + timedelta(minutes=20).total_seconds()
