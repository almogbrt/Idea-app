from __future__ import annotations

from pydantic import BaseModel, Field


class DriveFileView(BaseModel):
    id: str
    name: str
    mime_type: str
    web_view_link: str | None = None
    modified_time: str | None = None


class CreateFileRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    content: str = ""
    mime_type: str = "text/plain"


class ShareFileRequest(BaseModel):
    email: str = Field(..., min_length=3)
    role: str = "reader"


class FileContentView(BaseModel):
    content: str
