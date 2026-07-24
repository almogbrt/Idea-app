from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field


class IncomeRecordView(BaseModel):
    id: str
    date: str
    amount: float
    currency: str
    client_name: str | None
    description: str | None
    status: str
    green_invoice_client_id: str | None
    matched_client_id: uuid.UUID | None


class ExpenseRecordView(BaseModel):
    id: str
    date: str
    amount: float
    currency: str
    category: str | None
    description: str | None


class FinanceOverviewView(BaseModel):
    from_date: date
    to_date: date
    income: list[IncomeRecordView]
    expenses: list[ExpenseRecordView]
    total_income: float
    total_expenses: float
    net: float


class CashFlowSnapshotView(BaseModel):
    current_balance: float
    fixed_expenses_this_month: float
    dues_this_month: float
    projected_end_of_month_balance: float
    fetched_at: datetime


class LinkIncomeClientRequest(BaseModel):
    green_invoice_client_id: str = Field(..., min_length=1)
    green_invoice_client_name: str = Field(..., min_length=1)
    client_id: uuid.UUID
