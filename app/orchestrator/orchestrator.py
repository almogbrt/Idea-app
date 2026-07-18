"""The central Orchestrator.

Edith is a business operating system, not a chatbot: every incoming
natural-language command flows through here. This is the single use case
that ties conversation history, long-term memory retrieval, and the
Intent Router together, and persists the result.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.application.ports.agent_tool import ToolExecutionContext
from app.application.ports.conversation_repository import ConversationRepositoryPort
from app.application.ports.llm_gateway import LLMMessage
from app.application.use_cases.memory_use_cases import RetrieveMemoryUseCase, StoreMemoryUseCase
from app.core.exceptions import ExternalServiceError
from app.core.logging import bind_request_context, get_logger
from app.domain.entities import Message, MessageRole, OrchestrationResult
from app.orchestrator.intent_router import IntentRouter

logger = get_logger(__name__)

SYSTEM_PROMPT_TEMPLATE = """You are Edith, the business operating system for your one owner. \
You are not a chatbot: you take natural-language commands and get real work done through the \
tools available to you (Google Drive, Gmail, Calendar, Sheets, and any future agents). \
Always prefer calling a tool over guessing when a command implies a concrete action or lookup. \
Be concise, direct, and confirm what you did after acting.

Relevant long-term memory about the owner (may be empty):
{memory_context}
"""


class Orchestrator:
    def __init__(
        self,
        conversation_repository: ConversationRepositoryPort,
        intent_router: IntentRouter,
        retrieve_memory: RetrieveMemoryUseCase,
        store_memory: StoreMemoryUseCase,
        history_limit: int = 20,
    ) -> None:
        self._conversations = conversation_repository
        self._router = intent_router
        self._retrieve_memory = retrieve_memory
        self._store_memory = store_memory
        self._history_limit = history_limit

    async def handle_command(
        self, *, user_id: uuid.UUID, conversation_id: uuid.UUID, text: str
    ) -> OrchestrationResult:
        correlation_id = str(uuid.uuid4())
        bind_request_context(
            correlation_id=correlation_id,
            user_id=str(user_id),
            conversation_id=str(conversation_id),
        )
        logger.info("command_received", text_length=len(text))

        await self._conversations.append_message(
            Message(
                id=uuid.uuid4(),
                conversation_id=conversation_id,
                role=MessageRole.USER,
                content=text,
                created_at=datetime.now(UTC),
            )
        )

        memory_context = await self._retrieve_memory_safely(user_id, text)
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(memory_context=memory_context)

        history = await self._conversations.get_recent_messages(
            conversation_id, limit=self._history_limit
        )
        # A history-limit truncation can land inside an old turn's tool_use/
        # tool_result sequence, leaving a leading orphaned tool_result with no
        # tool_use in view — Anthropic's API rejects that shape too.
        while history and history[0].role == MessageRole.TOOL:
            history = history[1:]
        conversation_messages = [
            LLMMessage(
                role=m.role,
                content=m.content,
                tool_calls=tuple(m.tool_calls),
                tool_call_id=m.tool_call_id,
            )
            for m in history
        ]

        context = ToolExecutionContext(
            user_id=user_id, conversation_id=conversation_id, correlation_id=correlation_id
        )
        routing_result = await self._router.route(
            system_prompt=system_prompt, conversation=conversation_messages, context=context
        )

        for trace_message in routing_result.trace_messages:
            await self._conversations.append_message(
                Message(
                    id=uuid.uuid4(),
                    conversation_id=conversation_id,
                    role=trace_message.role,
                    content=trace_message.content,
                    created_at=datetime.now(UTC),
                    tool_calls=list(trace_message.tool_calls),
                    tool_call_id=trace_message.tool_call_id,
                )
            )

        await self._conversations.append_message(
            Message(
                id=uuid.uuid4(),
                conversation_id=conversation_id,
                role=MessageRole.ASSISTANT,
                content=routing_result.reply,
                created_at=datetime.now(UTC),
            )
        )

        await self._store_memory_safely(user_id, text)

        logger.info("command_handled", tool_calls=len(routing_result.tool_calls_made))
        return OrchestrationResult(
            reply=routing_result.reply,
            conversation_id=conversation_id,
            tool_calls_made=routing_result.tool_calls_made,
        )

    async def _retrieve_memory_safely(self, user_id: uuid.UUID, text: str) -> str:
        """Long-term memory is an enhancement, not a hard dependency — a down or
        misconfigured embeddings provider must not block Edith from responding
        at all."""
        try:
            memories = await self._retrieve_memory.execute(user_id, text, top_k=5)
        except ExternalServiceError as exc:
            logger.warning("memory_retrieval_unavailable", error=str(exc))
            return "(unavailable)"
        return "\n".join(f"- {m.content}" for m in memories) if memories else "(no relevant memory)"

    async def _store_memory_safely(self, user_id: uuid.UUID, text: str) -> None:
        try:
            await self._store_memory.execute(user_id, text, metadata={"source": "user_command"})
        except ExternalServiceError as exc:
            logger.warning("memory_storage_unavailable", error=str(exc))
