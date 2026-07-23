from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date

from app.domain.entities import ExpenseRecord, IncomeRecord


class GreenInvoicePort(ABC):
    """Read-only view of the user's Green Invoice (חשבונית ירוקה) account —
    goes straight to the Green Invoice API, bypassing the LLM tool-call loop
    (same reasoning as `CalendarPort`/`InboxPort`). No write methods exist:
    this integration never creates or edits invoices/expenses from IDEA OS."""

    @abstractmethod
    async def list_income(self, from_date: date, to_date: date) -> list[IncomeRecord]:
        """Income documents (invoices/receipts) dated within [from_date, to_date]."""
        raise NotImplementedError

    @abstractmethod
    async def list_expenses(self, from_date: date, to_date: date) -> list[ExpenseRecord]:
        """Expense records dated within [from_date, to_date]."""
        raise NotImplementedError
