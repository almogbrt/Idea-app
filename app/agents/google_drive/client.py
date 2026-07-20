"""Thin wrapper around the Google Drive v3 API for this agent's needs."""

from __future__ import annotations

import uuid
from typing import Any, cast

from googleapiclient.http import MediaInMemoryUpload

from app.agents._shared import call_google_api
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory

_LIST_FIELDS = "files(id,name,mimeType,webViewLink,modifiedTime)"


class DriveClient:
    def __init__(self, google_clients: GoogleApiClientFactory) -> None:
        self._google_clients = google_clients

    async def list_files(
        self,
        user_id: uuid.UUID,
        query: str | None,
        max_results: int,
        order_by: str | None = None,
    ) -> list[dict[str, Any]]:
        service = await self._google_clients.drive(user_id)
        response = await call_google_api(
            lambda: service.files()
            .list(q=query, pageSize=max_results, fields=_LIST_FIELDS, orderBy=order_by)
            .execute(),
            action="drive.files.list",
        )
        return cast(list[dict[str, Any]], response.get("files", []))

    async def get_file_content(self, user_id: uuid.UUID, file_id: str) -> str:
        service = await self._google_clients.drive(user_id)
        metadata = await call_google_api(
            lambda: service.files().get(fileId=file_id, fields="name,mimeType").execute(),
            action="drive.files.get",
        )
        mime_type = metadata["mimeType"]

        if mime_type.startswith("application/vnd.google-apps"):
            content_bytes = await call_google_api(
                lambda: service.files()
                .export(fileId=file_id, mimeType="text/plain")
                .execute(),
                action="drive.files.export",
            )
        else:
            content_bytes = await call_google_api(
                lambda: service.files().get_media(fileId=file_id).execute(),
                action="drive.files.get_media",
            )

        if isinstance(content_bytes, bytes):
            return content_bytes.decode("utf-8", errors="replace")
        return str(content_bytes)

    async def create_file(
        self, user_id: uuid.UUID, name: str, content: str, mime_type: str
    ) -> dict[str, Any]:
        service = await self._google_clients.drive(user_id)
        media = MediaInMemoryUpload(content.encode("utf-8"), mimetype=mime_type)
        return await call_google_api(
            lambda: service.files()
            .create(body={"name": name}, media_body=media, fields="id,name,webViewLink")
            .execute(),
            action="drive.files.create",
        )

    async def upload_binary_file(
        self, user_id: uuid.UUID, name: str, content: bytes, mime_type: str
    ) -> dict[str, Any]:
        service = await self._google_clients.drive(user_id)
        media = MediaInMemoryUpload(content, mimetype=mime_type)
        return await call_google_api(
            lambda: service.files()
            .create(body={"name": name}, media_body=media, fields="id,name")
            .execute(),
            action="drive.files.create_binary",
        )

    async def download_binary_file(self, user_id: uuid.UUID, file_id: str) -> tuple[bytes, str]:
        service = await self._google_clients.drive(user_id)
        metadata = await call_google_api(
            lambda: service.files().get(fileId=file_id, fields="mimeType").execute(),
            action="drive.files.get",
        )
        content = await call_google_api(
            lambda: service.files().get_media(fileId=file_id).execute(),
            action="drive.files.get_media",
        )
        return cast(bytes, content), cast(str, metadata["mimeType"])

    async def share_file(
        self, user_id: uuid.UUID, file_id: str, email: str, role: str
    ) -> dict[str, Any]:
        service = await self._google_clients.drive(user_id)
        return await call_google_api(
            lambda: service.permissions()
            .create(
                fileId=file_id,
                body={"type": "user", "role": role, "emailAddress": email},
                fields="id",
                sendNotificationEmail=False,
            )
            .execute(),
            action="drive.permissions.create",
        )
