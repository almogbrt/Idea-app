"""Endpoints meant to be called by trusted infrastructure, not a logged-in
user — currently just Cloud Scheduler, hourly, to check due reminders.

There is no session here, so authentication is a shared secret header
instead of the usual `idea_os_session` cookie.
"""

from __future__ import annotations

import hmac

from fastapi import APIRouter, Depends, Header

from app.core.config import Settings, get_settings
from app.core.container import RequestScopedServices
from app.core.exceptions import AuthError
from app.interfaces.api.dependencies import get_request_scope
from app.interfaces.api.schemas.workspace import RunRemindersResponse

router = APIRouter(prefix="/internal", tags=["internal"])

_SCHEDULER_SECRET_HEADER = "X-Scheduler-Secret"


def _verify_scheduler_secret(
    x_scheduler_secret: str | None = Header(default=None, alias=_SCHEDULER_SECRET_HEADER),
    settings: Settings = Depends(get_settings),
) -> None:
    expected = settings.scheduler_shared_secret
    provided = x_scheduler_secret or ""
    if not expected or not hmac.compare_digest(provided, expected):
        raise AuthError("Missing or invalid scheduler secret.")


@router.post(
    "/reminders/run",
    response_model=RunRemindersResponse,
    dependencies=[Depends(_verify_scheduler_secret)],
)
async def run_reminders(
    scope: RequestScopedServices = Depends(get_request_scope),
) -> RunRemindersResponse:
    raised = await scope.check_reminders.execute()
    return RunRemindersResponse(notifications_raised=raised)
