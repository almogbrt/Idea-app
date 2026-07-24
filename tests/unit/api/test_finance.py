from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.application.use_cases.cash_flow import CashFlowUseCase
from app.application.use_cases.finance_overview import FinanceOverviewUseCase
from app.core.container import RequestScopedServices
from app.domain.entities import CashFlowSnapshot, ExpenseRecord, IncomeRecord, User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from tests.conftest import (
    FakeCache,
    FakeCashFlowPort,
    FakeClientRepository,
    FakeGreenInvoicePort,
    FakeIncomeClientLinkRepository,
)

_USER = User(
    id=uuid.uuid4(),
    google_sub="sub-finance",
    email="owner@example.com",
    name="Owner",
    created_at=datetime.now(UTC),
)


def _install_scope(client: TestClient) -> dict[str, object]:
    green_invoice = FakeGreenInvoicePort()
    clients_repo = FakeClientRepository()
    cache = FakeCache()
    cash_flow_port = FakeCashFlowPort()
    income_client_links = FakeIncomeClientLinkRepository()

    scope = RequestScopedServices(
        orchestrator=None,  # type: ignore[arg-type]
        manage_conversation=None,  # type: ignore[arg-type]
        authenticate_user=None,  # type: ignore[arg-type]
        manage_clients=None,  # type: ignore[arg-type]
        manage_projects=None,  # type: ignore[arg-type]
        manage_tasks=None,  # type: ignore[arg-type]
        manage_thoughts=None,  # type: ignore[arg-type]
        manage_whatsapp_messages=None,  # type: ignore[arg-type]
        dashboard_summary=None,  # type: ignore[arg-type]
        list_activity=None,  # type: ignore[arg-type]
        manage_notifications=None,  # type: ignore[arg-type]
        check_reminders=None,  # type: ignore[arg-type]
        send_daily_review=None,  # type: ignore[arg-type]
        manage_calendar=None,  # type: ignore[arg-type]
        manage_email=None,  # type: ignore[arg-type]
        manage_files=None,  # type: ignore[arg-type]
        manage_goals=None,  # type: ignore[arg-type]
        manage_daily_plan=None,  # type: ignore[arg-type]
        manage_focus_sessions=None,  # type: ignore[arg-type]
        daily_plan_metrics=None,  # type: ignore[arg-type]
        finance_overview=FinanceOverviewUseCase(
            green_invoice, clients_repo, cache, income_client_links
        ),
        cash_flow=CashFlowUseCase(cash_flow_port),
    )
    client.app.dependency_overrides[get_current_user] = lambda: _USER
    client.app.dependency_overrides[get_request_scope] = lambda: scope
    return {
        "green_invoice": green_invoice,
        "clients_repo": clients_repo,
        "cache": cache,
        "cash_flow_port": cash_flow_port,
        "income_client_links": income_client_links,
    }


def test_overview_defaults_to_current_month(client: TestClient) -> None:
    resources = _install_scope(client)
    green_invoice: FakeGreenInvoicePort = resources["green_invoice"]  # type: ignore[assignment]
    green_invoice.income = [
        IncomeRecord(
            id="doc-1", date="2026-07-05", amount=1000.0, currency="ILS",
            client_name=None, description=None, status="OPENED_DOCUMENT",
        ),
    ]
    green_invoice.expenses = [
        ExpenseRecord(id="exp-1", date="2026-07-06", amount=200.0, currency="ILS",
                      category=None, description=None),
    ]

    response = client.get("/api/v1/finance/overview")

    assert response.status_code == 200
    body = response.json()
    assert body["total_income"] == 1000.0
    assert body["total_expenses"] == 200.0
    assert body["net"] == 800.0
    assert len(body["income"]) == 1
    assert len(body["expenses"]) == 1


def test_overview_accepts_explicit_date_range(client: TestClient) -> None:
    resources = _install_scope(client)
    green_invoice: FakeGreenInvoicePort = resources["green_invoice"]  # type: ignore[assignment]
    green_invoice.income = [
        IncomeRecord(
            id="doc-1", date="2026-01-15", amount=500.0, currency="ILS",
            client_name="לקוח", description=None, status="OPENED_DOCUMENT",
        ),
    ]

    response = client.get(
        "/api/v1/finance/overview", params={"from_date": "2026-01-01", "to_date": "2026-01-31"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["from_date"] == "2026-01-01"
    assert body["to_date"] == "2026-01-31"
    assert body["income"][0]["client_name"] == "לקוח"


def test_overview_matches_income_to_existing_client(client: TestClient) -> None:
    resources = _install_scope(client)
    client_repo: FakeClientRepository = resources["clients_repo"]  # type: ignore[assignment]
    matched_client = asyncio.run(client_repo.create(_USER.id, "לקוח קיים"))
    green_invoice: FakeGreenInvoicePort = resources["green_invoice"]  # type: ignore[assignment]
    green_invoice.income = [
        IncomeRecord(
            id="doc-1", date="2026-07-05", amount=300.0, currency="ILS",
            client_name="לקוח קיים", description=None, status="OPENED_DOCUMENT",
        ),
    ]

    response = client.get("/api/v1/finance/overview")

    assert response.status_code == 200
    body = response.json()
    assert body["income"][0]["matched_client_id"] == str(matched_client.id)


def test_link_income_client_persists_manual_match(client: TestClient) -> None:
    resources = _install_scope(client)
    client_repo: FakeClientRepository = resources["clients_repo"]  # type: ignore[assignment]
    target_client = asyncio.run(client_repo.create(_USER.id, "לקוח אמיתי"))
    green_invoice: FakeGreenInvoicePort = resources["green_invoice"]  # type: ignore[assignment]
    green_invoice.income = [
        IncomeRecord(
            id="doc-1", date="2026-07-05", amount=1770.0, currency="ILS",
            client_name="שם אחר בחשבונית ירוקה", description=None, status="1",
            green_invoice_client_id="gi-client-1",
        ),
    ]

    link_response = client.post(
        "/api/v1/finance/link-client",
        json={
            "green_invoice_client_id": "gi-client-1",
            "green_invoice_client_name": "שם אחר בחשבונית ירוקה",
            "client_id": str(target_client.id),
        },
    )
    assert link_response.status_code == 204

    response = client.get("/api/v1/finance/overview")

    assert response.status_code == 200
    assert response.json()["income"][0]["matched_client_id"] == str(target_client.id)


def test_cash_flow_returns_null_when_not_configured(client: TestClient) -> None:
    _install_scope(client)

    response = client.get("/api/v1/finance/cash-flow")

    assert response.status_code == 200
    assert response.json() is None


def test_cash_flow_returns_snapshot_when_available(client: TestClient) -> None:
    resources = _install_scope(client)
    cash_flow_port: FakeCashFlowPort = resources["cash_flow_port"]  # type: ignore[assignment]
    cash_flow_port.snapshot = CashFlowSnapshot(
        current_balance=-23622.0,
        fixed_expenses_this_month=-2510.0,
        dues_this_month=-4617.46,
        projected_end_of_month_balance=-30201.0,
        fetched_at=datetime.now(UTC),
    )

    response = client.get("/api/v1/finance/cash-flow")

    assert response.status_code == 200
    body = response.json()
    assert body["current_balance"] == -23622.0
    assert body["dues_this_month"] == -4617.46
