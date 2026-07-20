from __future__ import annotations

from app.agents.whatsapp.service import WhatsAppService
from app.agents.whatsapp.tools import GetWhatsAppConversationTool, SendWhatsAppMessageTool
from app.application.ports.agent_tool import Tool
from app.orchestrator.base_agent import BaseAgent


class WhatsAppAgent(BaseAgent):
    name = "whatsapp"
    description = "Reads and sends WhatsApp messages with the user's clients."

    def __init__(self, service: WhatsAppService) -> None:
        self._service = service

    def get_tools(self) -> list[Tool]:
        return [
            GetWhatsAppConversationTool(self._service),
            SendWhatsAppMessageTool(self._service),
        ]
