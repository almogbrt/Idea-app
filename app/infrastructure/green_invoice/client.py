"""Thin read-only wrapper around the Green Invoice (חשבונית ירוקה) API.

There's exactly one Green Invoice account for the whole app (Almog's own
business), not one per user — a single API id/secret pair configured via
`Settings`, not a per-user OAuth token. This client is a `Container`-level
singleton, not built per request.

This client never creates, updates, or deletes anything in Green Invoice —
only `documents/search` and `expenses/search` are ever called.
"""

from __future__ import annotations

import time
from datetime import date
from typing import Any, cast

import httpx
import jwt

from app.application.ports.green_invoice_port import GreenInvoicePort
from app.core.exceptions import AuthError, ExternalServiceError
from app.core.logging import get_logger
from app.domain.entities import ExpenseRecord, IncomeRecord

logger = get_logger(__name__)

_TOKEN_REFRESH_MARGIN_SECONDS = 60
"""Refetch the token this many seconds before its real expiry, so a
request never starts with a token that expires mid-flight."""


class GreenInvoiceClient(GreenInvoicePort):
    def __init__(self, api_id: str, api_secret: str, base_url: str) -> None:
        self._api_id = api_id
        self._api_secret = api_secret
        self._base_url = base_url.rstrip("/")
        self._token: str | None = None
        self._token_expires_at: float = 0.0

    async def list_income(self, from_date: date, to_date: date) -> list[IncomeRecord]:
        """`/documents/search` returns every document type in range, not just
        realized income — price quotes and orders are pre-sale drafts with
        no money actually received, so including them roughly doubled the
        reported total. Filtering happens client-side on each item's own
        `type` field (see `_parse_income`) rather than via a search-request
        filter, since the exact request-side filter parameter isn't
        documented publicly and every returned document reliably carries
        its own type."""
        body = await self._post(
            "/documents/search",
            {"fromDate": from_date.isoformat(), "toDate": to_date.isoformat()},
        )
        records = (_parse_income(item) for item in body.get("items", []))
        return [record for record in records if record is not None]

    async def list_expenses(self, from_date: date, to_date: date) -> list[ExpenseRecord]:
        body = await self._post(
            "/expenses/search",
            {"fromDate": from_date.isoformat(), "toDate": to_date.isoformat()},
        )
        return [_parse_expense(item) for item in body.get("items", [])]

    async def _post(self, path: str, json_body: dict[str, Any]) -> dict[str, Any]:
        token = await self._get_token()
        url = f"{self._base_url}{path}"
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.post(
                    url, json=json_body, headers={"Authorization": f"Bearer {token}"}
                )
                response.raise_for_status()
                return cast(dict[str, Any], response.json())
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "green_invoice_api_error",
                    status=exc.response.status_code,
                    body=exc.response.text,
                )
                if exc.response.status_code == httpx.codes.UNAUTHORIZED:
                    raise AuthError("Green Invoice rejected the API credentials.") from exc
                raise ExternalServiceError(
                    f"Green Invoice API error calling {path}: {exc.response.text}"
                ) from exc
            except httpx.HTTPError as exc:
                logger.error("green_invoice_api_error", error=str(exc))
                raise ExternalServiceError(f"Green Invoice API request failed: {exc}") from exc

    async def _get_token(self) -> str:
        if self._token is not None and time.time() < self._token_expires_at:
            return self._token
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.post(
                    f"{self._base_url}/account/token",
                    json={"id": self._api_id, "secret": self._api_secret},
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                logger.error(
                    "green_invoice_auth_error",
                    status=exc.response.status_code,
                    body=exc.response.text,
                )
                raise AuthError("Green Invoice rejected the API credentials.") from exc
            except httpx.HTTPError as exc:
                logger.error("green_invoice_auth_error", error=str(exc))
                raise ExternalServiceError(f"Green Invoice auth request failed: {exc}") from exc
        token = str(response.json()["token"])
        self._token = token
        self._token_expires_at = _token_expiry(token) - _TOKEN_REFRESH_MARGIN_SECONDS
        return token


def _token_expiry(token: str) -> float:
    """Reads the `exp` claim without signature verification — we trust the
    issuer (we just fetched it over TLS), we only need the expiry time so we
    know when to refetch. Falls back to a conservative 25 minutes if the
    claim is somehow missing."""
    try:
        claims = jwt.decode(token, options={"verify_signature": False})
        exp = claims.get("exp")
        if isinstance(exp, int | float):
            return float(exp)
    except jwt.PyJWTError:
        pass
    return time.time() + 25 * 60


_NON_INCOME_DOCUMENT_TYPES = frozenset({10, 100, 200, 210, 300})
"""Price quote, order, delivery note, return delivery note — pre-sale
documents with no money actually received; not real income. Type 300
("Transaction Account") is different: confirmed against a real account
(see commit history) that Green Invoice auto-generates one of these
alongside every real sale document (e.g. type 320) as an internal
accounting-ledger mirror, carrying the *same* amount — counting both
double-counts a single sale."""

_CREDIT_INVOICE_DOCUMENT_TYPE = 330
"""A refund/credit note — reduces income, isn't additional income."""


def _parse_income(item: dict[str, Any]) -> IncomeRecord | None:
    doc_type = item.get("type")
    if doc_type in _NON_INCOME_DOCUMENT_TYPES:
        return None
    client = item.get("client")
    client_name = client.get("name") if isinstance(client, dict) else None
    client_id = client.get("id") if isinstance(client, dict) else None
    description = item.get("description") or item.get("remarks")
    amount = float(item.get("amount", 0) or 0)
    if doc_type == _CREDIT_INVOICE_DOCUMENT_TYPE:
        amount = -abs(amount)
    return IncomeRecord(
        id=str(item.get("id", "")),
        date=str(item.get("date", "")),
        amount=amount,
        currency=str(item.get("currency", "ILS")),
        client_name=str(client_name) if client_name is not None else None,
        description=str(description) if description is not None else None,
        status=str(item.get("status", "")),
        green_invoice_client_id=str(client_id) if client_id is not None else None,
    )


def _parse_expense(item: dict[str, Any]) -> ExpenseRecord:
    """Green Invoice's `/expenses/search` response shape has no confirmed
    public schema (unlike documents/clients, which come from a verified
    third-party typed wrapper) — parsed defensively with fallbacks. Field
    names here (`amount`/`date`/`category`/`description`) should be
    double-checked against a real response once the integration is live."""
    category = item.get("category")
    description = item.get("description") or item.get("remarks")
    return ExpenseRecord(
        id=str(item.get("id", "")),
        date=str(item.get("date", item.get("valueDate", ""))),
        amount=float(item.get("amount", item.get("price", 0)) or 0),
        currency=str(item.get("currency", "ILS")),
        category=str(category) if category is not None else None,
        description=str(description) if description is not None else None,
    )
