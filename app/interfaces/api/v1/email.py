"""Dashboard inbox endpoint — goes straight to the Gmail API via
`ManageEmailUseCase`, bypassing the LLM tool-call loop (same reasoning as
`app/interfaces/api/v1/workspace.py`). Edith can still manage the same
inbox through natural language via the `gmail` Agent.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.container import RequestScopedServices
from app.domain.entities import EmailSummary, User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from app.interfaces.api.schemas.email import EmailView

router = APIRouter(prefix="/emails", tags=["email"])


def _email_view(email: EmailSummary) -> EmailView:
    return EmailView(
        id=email.id,
        sender=email.sender,
        subject=email.subject,
        snippet=email.snippet,
        date=email.date,
    )


@router.get("", response_model=list[EmailView])
async def list_emails(
    max_results: int = 4,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> list[EmailView]:
    emails = await scope.manage_email.list_recent(user.id, max_results)
    return [_email_view(e) for e in emails]
