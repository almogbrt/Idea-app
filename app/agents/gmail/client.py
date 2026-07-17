"""Thin wrapper around the Gmail v1 API for this agent's needs."""

from __future__ import annotations

import base64
import uuid
from email.mime.text import MIMEText
from typing import Any

from app.agents._shared import call_google_api
from app.infrastructure.google.api_client_factory import GoogleApiClientFactory

_METADATA_HEADERS = ["From", "Subject", "Date"]


class GmailClient:
    def __init__(self, google_clients: GoogleApiClientFactory) -> None:
        self._google_clients = google_clients

    async def list_messages(
        self, user_id: uuid.UUID, query: str | None, max_results: int
    ) -> list[dict[str, Any]]:
        service = await self._google_clients.gmail(user_id)
        list_response = await call_google_api(
            lambda: service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute(),
            action="gmail.messages.list",
        )
        async def fetch_metadata(message_id: str) -> dict[str, Any]:
            return await call_google_api(
                lambda: service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="metadata",
                    metadataHeaders=_METADATA_HEADERS,
                )
                .execute(),
                action="gmail.messages.get",
            )

        summaries: list[dict[str, Any]] = []
        for item in list_response.get("messages", []):
            message = await fetch_metadata(item["id"])
            headers = {
                h["name"]: h["value"] for h in message.get("payload", {}).get("headers", [])
            }
            summaries.append(
                {
                    "id": message["id"],
                    "snippet": message.get("snippet", ""),
                    "from": headers.get("From", ""),
                    "subject": headers.get("Subject", ""),
                    "date": headers.get("Date", ""),
                }
            )
        return summaries

    async def get_message(self, user_id: uuid.UUID, message_id: str) -> dict[str, Any]:
        service = await self._google_clients.gmail(user_id)
        message = await call_google_api(
            lambda: service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute(),
            action="gmail.messages.get",
        )
        headers = {h["name"]: h["value"] for h in message.get("payload", {}).get("headers", [])}
        return {
            "id": message["id"],
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
            "body": self._extract_body(message.get("payload", {})),
        }

    @staticmethod
    def _extract_body(payload: dict[str, Any]) -> str:
        if payload.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(payload["body"]["data"]).decode(
                "utf-8", errors="replace"
            )
        for part in payload.get("parts", []):
            if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
                return base64.urlsafe_b64decode(part["body"]["data"]).decode(
                    "utf-8", errors="replace"
                )
        return ""

    async def send_message(
        self, user_id: uuid.UUID, to: str, subject: str, body: str
    ) -> dict[str, Any]:
        service = await self._google_clients.gmail(user_id)
        mime_message = MIMEText(body)
        mime_message["to"] = to
        mime_message["subject"] = subject
        raw = base64.urlsafe_b64encode(mime_message.as_bytes()).decode("utf-8")
        return await call_google_api(
            lambda: service.users().messages().send(userId="me", body={"raw": raw}).execute(),
            action="gmail.messages.send",
        )
