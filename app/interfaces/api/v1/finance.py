"""Dashboard finance section — read-only Green Invoice income/expense
overview. Goes straight to `FinanceOverviewUseCase`, bypassing the LLM
tool-call loop (same reasoning as `calendar.py`/`workspace.py`). There is no
chat tool for this, and no write endpoints: IDEA OS never creates or edits
anything in Green Invoice, it only displays what's already there.
"""

from __future__ import annotations

from datetime import UTC, date, datetime

from fastapi import APIRouter, Depends

from app.core.container import RequestScopedServices
from app.domain.entities import CashFlowSnapshot, ExpenseRecord, FinanceOverview, IncomeRecord, User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from app.interfaces.api.schemas.finance import (
    CashFlowSnapshotView,
    ExpenseRecordView,
    FinanceOverviewView,
    IncomeRecordView,
    LinkIncomeClientRequest,
)

router = APIRouter(prefix="/finance", tags=["finance"])


def _income_view(record: IncomeRecord) -> IncomeRecordView:
    return IncomeRecordView(
        id=record.id,
        date=record.date,
        amount=record.amount,
        currency=record.currency,
        client_name=record.client_name,
        description=record.description,
        status=record.status,
        green_invoice_client_id=record.green_invoice_client_id,
        matched_client_id=record.matched_client_id,
    )


def _expense_view(record: ExpenseRecord) -> ExpenseRecordView:
    return ExpenseRecordView(
        id=record.id,
        date=record.date,
        amount=record.amount,
        currency=record.currency,
        category=record.category,
        description=record.description,
    )


def _overview_view(overview: FinanceOverview) -> FinanceOverviewView:
    return FinanceOverviewView(
        from_date=overview.from_date,
        to_date=overview.to_date,
        income=[_income_view(r) for r in overview.income],
        expenses=[_expense_view(r) for r in overview.expenses],
        total_income=overview.total_income,
        total_expenses=overview.total_expenses,
        net=overview.net,
    )


@router.get("/overview", response_model=FinanceOverviewView)
async def get_overview(
    from_date: str | None = None,
    to_date: str | None = None,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> FinanceOverviewView:
    """Defaults to the current calendar month if no range is given."""
    today = datetime.now(UTC).date()
    range_start = today.replace(day=1) if from_date is None else _parse_date(from_date)
    range_end = today if to_date is None else _parse_date(to_date)
    overview = await scope.finance_overview.get_overview(user.id, range_start, range_end)
    return _overview_view(overview)


def _parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


@router.post("/link-client", status_code=204)
async def link_income_client(
    body: LinkIncomeClientRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> None:
    """Manually links a Green Invoice client (by its own id, not name) to an
    existing IDEA OS client — for income that doesn't auto-match by name."""
    await scope.finance_overview.link_income_client(
        user.id, body.green_invoice_client_id, body.green_invoice_client_name, body.client_id
    )


def _cash_flow_view(snapshot: CashFlowSnapshot) -> CashFlowSnapshotView:
    return CashFlowSnapshotView(
        current_balance=snapshot.current_balance,
        fixed_expenses_this_month=snapshot.fixed_expenses_this_month,
        dues_this_month=snapshot.dues_this_month,
        projected_end_of_month_balance=snapshot.projected_end_of_month_balance,
        fetched_at=snapshot.fetched_at,
    )


@router.get("/cash-flow", response_model=CashFlowSnapshotView | None)
async def get_cash_flow(
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> CashFlowSnapshotView | None:
    snapshot = await scope.cash_flow.get_snapshot(user.id)
    return _cash_flow_view(snapshot) if snapshot else None
