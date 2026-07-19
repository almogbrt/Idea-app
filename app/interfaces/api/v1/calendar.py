"""Dashboard calendar endpoints — go straight to the Calendar API via
`ManageCalendarUseCase`, bypassing the LLM tool-call loop (same reasoning as
`app/interfaces/api/v1/workspace.py`). Edith can still manage the same
calendar through natural language via the `google_calendar` Agent.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends

from app.core.container import RequestScopedServices
from app.domain.entities import CalendarEvent, User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from app.interfaces.api.schemas.calendar import CalendarEventView, CreateCalendarEventRequest

router = APIRouter(prefix="/calendar", tags=["calendar"])


def _event_view(event: CalendarEvent) -> CalendarEventView:
    return CalendarEventView(
        id=event.id,
        summary=event.summary,
        start=event.start,
        end=event.end,
        description=event.description,
        html_link=event.html_link,
    )


@router.get("/events", response_model=list[CalendarEventView])
async def list_events(
    time_min: str | None = None,
    time_max: str | None = None,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> list[CalendarEventView]:
    """Defaults to "today" (server-side UTC) if no range is given — the
    dashboard always passes an explicit browser-local range instead, for
    both the today card and the full month view."""
    if time_min is None or time_max is None:
        start_of_day = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
        time_min = start_of_day.isoformat()
        time_max = (start_of_day + timedelta(days=1)).isoformat()
    events = await scope.manage_calendar.list_between(user.id, time_min, time_max)
    return [_event_view(e) for e in events]


@router.post("/events", response_model=CalendarEventView)
async def create_event(
    body: CreateCalendarEventRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> CalendarEventView:
    event = await scope.manage_calendar.create(
        user.id, body.summary, body.start_time, body.end_time, body.description
    )
    return _event_view(event)


@router.delete("/events/{event_id}", status_code=204)
async def delete_event(
    event_id: str,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> None:
    await scope.manage_calendar.delete(user.id, event_id)
