from __future__ import annotations

import uuid
from datetime import date

from pydantic import BaseModel


class IncomeRecordView(BaseModel):
    id: str
    date: str
    amount: float
    currency: str
    client_name: str | None
    description: str | None
    status: str
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
