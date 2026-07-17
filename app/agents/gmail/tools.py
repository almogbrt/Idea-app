from __future__ import annotations

import json
from typing import Any

from app.agents.gmail.client import GmailClient
from app.application.ports.agent_tool import Tool, ToolExecutionContext
from app.domain.entities import ToolResult

AGENT_NAME = "gmail"


class ListRecentEmailsTool(Tool):
    name = "gmail_list_recent_emails"
    description = (
        "List or search the user's Gmail messages. `query` accepts native Gmail search syntax "
        "(e.g. 'from:boss@company.com is:unread', 'subject:invoice after:2026/01/01')."
    )
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Gmail search query (optional)."},
            "max_results": {
                "type": "integer",
                "description": "Maximum number of emails to return.",
                "default": 10,
            },
        },
        "required": [],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: GmailClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        messages = await self._client.list_messages(
            context.user_id, arguments.get("query"), arguments.get("max_results", 10)
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(messages))


class GetEmailTool(Tool):
    name = "gmail_get_email"
    description = "Get the full content (from, subject, date, body) of one Gmail message by ID."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {"message_id": {"type": "string", "description": "Gmail message ID."}},
        "required": ["message_id"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: GmailClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        message = await self._client.get_message(context.user_id, arguments["message_id"])
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(message))


class SendEmailTool(Tool):
    name = "gmail_send_email"
    description = "Send an email from the user's Gmail account."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "to": {"type": "string", "description": "Recipient email address."},
            "subject": {"type": "string", "description": "Email subject."},
            "body": {"type": "string", "description": "Email body (plain text)."},
        },
        "required": ["to", "subject", "body"],
    }
    agent_name = AGENT_NAME

    def __init__(self, client: GmailClient) -> None:
        self._client = client

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        result = await self._client.send_message(
            context.user_id, arguments["to"], arguments["subject"], arguments["body"]
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content=json.dumps(result))
