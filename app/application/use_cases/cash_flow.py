from __future__ import annotations

import uuid

from app.application.ports.cash_flow_port import CashFlowPort
from app.domain.entities import CashFlowSnapshot


class CashFlowUseCase:
    def __init__(self, cash_flow_port: CashFlowPort) -> None:
        self._port = cash_flow_port

    async def get_snapshot(self, user_id: uuid.UUID) -> CashFlowSnapshot | None:
        return await self._port.get_snapshot(user_id)
