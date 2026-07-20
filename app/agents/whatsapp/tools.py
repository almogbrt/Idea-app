from __future__ import annotations

from typing import Any

from app.agents.whatsapp.service import WhatsAppService
from app.application.ports.agent_tool import Tool, ToolExecutionContext
from app.domain.entities import ToolResult

AGENT_NAME = "whatsapp"


class GetWhatsAppConversationTool(Tool):
    name = "whatsapp_get_conversation"
    description = (
        "Read the recent WhatsApp message history with a client, so you can summarize it "
        "or extract action items (e.g. create tasks) from it. Only call this when the user "
        "explicitly asks you to look at a WhatsApp conversation — never proactively."
    )
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "client_name": {
                "type": "string",
                "description": "Name (or part of it) of the client whose conversation to read.",
            },
        },
        "required": ["client_name"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WhatsAppService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        transcript = await self._service.get_conversation(context.user_id, arguments["client_name"])
        return ToolResult(tool_call_id="", tool_name=self.name, content=transcript)


class SendWhatsAppMessageTool(Tool):
    name = "whatsapp_send_message"
    description = "Send a WhatsApp message to a client."
    parameters_schema: dict[str, Any] = {
        "type": "object",
        "properties": {
            "client_name": {
                "type": "string",
                "description": "Name (or part of it) of the client to message.",
            },
            "message": {"type": "string", "description": "The message text to send."},
        },
        "required": ["client_name", "message"],
    }
    agent_name = AGENT_NAME

    def __init__(self, service: WhatsAppService) -> None:
        self._service = service

    async def execute(self, arguments: dict[str, Any], context: ToolExecutionContext) -> ToolResult:
        await self._service.send_message(
            context.user_id, arguments["client_name"], arguments["message"]
        )
        return ToolResult(tool_call_id="", tool_name=self.name, content="Message sent.")
