from __future__ import annotations

import uuid
from typing import Any

from app.agents.whatsapp.tools import GetWhatsAppConversationTool, SendWhatsAppMessageTool
from app.application.ports.agent_tool import ToolExecutionContext


class _FakeWhatsAppService:
    def __init__(self) -> None:
        self.calls: list[tuple[str, tuple[Any, ...]]] = []

    async def get_conversation(self, user_id: uuid.UUID, client_name: str, limit: int = 50) -> str:
        self.calls.append(("get_conversation", (user_id, client_name, limit)))
        return "[them] hi\n[you] hello"

    async def send_message(self, user_id: uuid.UUID, client_name: str, message: str) -> None:
        self.calls.append(("send_message", (user_id, client_name, message)))


def _context() -> ToolExecutionContext:
    return ToolExecutionContext(
        user_id=uuid.uuid4(), conversation_id=uuid.uuid4(), correlation_id="corr"
    )


async def test_get_whatsapp_conversation_tool() -> None:
    service = _FakeWhatsAppService()
    tool = GetWhatsAppConversationTool(service)
    context = _context()

    result = await tool.execute({"client_name": "Baron's"}, context)

    assert service.calls == [("get_conversation", (context.user_id, "Baron's", 50))]
    assert result.content == "[them] hi\n[you] hello"


async def test_send_whatsapp_message_tool() -> None:
    service = _FakeWhatsAppService()
    tool = SendWhatsAppMessageTool(service)
    context = _context()

    result = await tool.execute(
        {"client_name": "Baron's", "message": "Running 10 min late"}, context
    )

    assert service.calls == [
        ("send_message", (context.user_id, "Baron's", "Running 10 min late"))
    ]
    assert result.content == "Message sent."


def test_tool_definitions_expose_valid_json_schema() -> None:
    service = _FakeWhatsAppService()
    for tool in [GetWhatsAppConversationTool(service), SendWhatsAppMessageTool(service)]:
        definition = tool.definition()
        assert definition.name == tool.name
        assert definition.parameters_schema["type"] == "object"
        assert definition.agent_name == "whatsapp"
