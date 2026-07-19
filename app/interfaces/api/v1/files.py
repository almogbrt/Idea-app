"""Dashboard files endpoints — go straight to the Drive API via
`ManageFilesUseCase`, bypassing the LLM tool-call loop (same reasoning as
`app/interfaces/api/v1/workspace.py`). Edith can still manage the same
files through natural language via the `google_drive` Agent.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.core.container import RequestScopedServices
from app.domain.entities import DriveFile, User
from app.interfaces.api.dependencies import get_current_user, get_request_scope
from app.interfaces.api.schemas.files import (
    CreateFileRequest,
    DriveFileView,
    FileContentView,
    ShareFileRequest,
)

router = APIRouter(prefix="/files", tags=["files"])


def _file_view(file: DriveFile) -> DriveFileView:
    return DriveFileView(
        id=file.id,
        name=file.name,
        mime_type=file.mime_type,
        web_view_link=file.web_view_link,
        modified_time=file.modified_time,
    )


@router.get("", response_model=list[DriveFileView])
async def list_files(
    query: str | None = None,
    max_results: int = 50,
    order_by: str | None = None,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> list[DriveFileView]:
    files = await scope.manage_files.list_files(user.id, query, max_results, order_by)
    return [_file_view(f) for f in files]


@router.get("/{file_id}/content", response_model=FileContentView)
async def get_file_content(
    file_id: str,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> FileContentView:
    content = await scope.manage_files.get_content(user.id, file_id)
    return FileContentView(content=content)


@router.post("", response_model=DriveFileView)
async def create_file(
    body: CreateFileRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> DriveFileView:
    file = await scope.manage_files.create_file(user.id, body.name, body.content, body.mime_type)
    return _file_view(file)


@router.post("/{file_id}/share", status_code=204)
async def share_file(
    file_id: str,
    body: ShareFileRequest,
    user: User = Depends(get_current_user),
    scope: RequestScopedServices = Depends(get_request_scope),
) -> None:
    await scope.manage_files.share_file(user.id, file_id, body.email, body.role)
