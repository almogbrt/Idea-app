"""OpenAI embeddings adapter for `EmbeddingPort`.

Anthropic has no embeddings endpoint, so long-term memory uses OpenAI's
embedding models regardless of which provider drives the chat/tool-use loop.
"""

from __future__ import annotations

import openai
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.application.ports.embedding import EmbeddingPort
from app.core.exceptions import ExternalServiceError
from app.core.logging import get_logger

logger = get_logger(__name__)

_RETRYABLE_EXCEPTIONS = (
    openai.APIConnectionError,
    openai.RateLimitError,
    openai.InternalServerError,
)


class OpenAIEmbeddingGateway(EmbeddingPort):
    def __init__(self, api_key: str, model: str) -> None:
        self._client = openai.AsyncOpenAI(api_key=api_key)
        self._model = model

    async def embed(self, text: str) -> list[float]:
        try:
            response = await self._call_with_retry(text)
        except openai.APIError as exc:
            logger.error("openai_embeddings_api_error", error=str(exc))
            raise ExternalServiceError(f"OpenAI embeddings API error: {exc}") from exc
        return list(response.data[0].embedding)

    @retry(
        retry=retry_if_exception_type(_RETRYABLE_EXCEPTIONS),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def _call_with_retry(self, text: str) -> openai.types.CreateEmbeddingResponse:
        return await self._client.embeddings.create(model=self._model, input=text)
