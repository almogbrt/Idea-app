from __future__ import annotations

import json
import uuid
from typing import Any

from app.agents.gmail.tools import GetEmailTool, ListRecentEmailsTool, SendEmailTool
from app.application.ports.agent_tool import ToolExecutionContext


class _FakeGmailClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def list_messages(
        self, user_id: uuid.UUID, query: str | None, max_results: int
    ) -> list[dict]:
        self.calls.append(("list_messages", (user_id, query, max_results)))
        return [{"id": "msg-1", "subject": "Hello"}]

    async def get_message(self, user_id: uuid.UUID, message_id: str) -> dict:
        self.calls.append(("get_message", (user_id, message_id)))
        return {"id": message_id, "body": "full body text"}

    async def send_message(self, user_id: uuid.UUID, to: str, subject: str, body: str) -> dict:
        self.calls.append(("send_message", (user_id, to, subject, body)))
        return {"id": "sent-1"}


def _context() -> ToolExecutionContext:
    return ToolExecutionContext(
        user_id=uuid.uuid4(), conversation_id=uuid.uuid4(), correlation_id="corr"
    )


async def test_list_recent_emails_tool() -> None:
    client = _FakeGmailClient()
    tool = ListRecentEmailsTool(client)
    context = _context()

    result = await tool.execute({"query": "is:unread", "max_results": 3}, context)

    assert client.calls == [("list_messages", (context.user_id, "is:unread", 3))]
    assert json.loads(result.content) == [{"id": "msg-1", "subject": "Hello"}]


async def test_get_email_tool() -> None:
    client = _FakeGmailClient()
    tool = GetEmailTool(client)
    context = _context()

    result = await tool.execute({"message_id": "msg-1"}, context)

    assert json.loads(result.content)["body"] == "full body text"


async def test_send_email_tool_requires_all_fields() -> None:
    client = _FakeGmailClient()
    tool = SendEmailTool(client)
    context = _context()

    await tool.execute(
        {"to": "someone@example.com", "subject": "Hi", "body": "text body"}, context
    )

    assert client.calls == [
        ("send_message", (context.user_id, "someone@example.com", "Hi", "text body"))
    ]
