from __future__ import annotations

import uuid

from app.application.use_cases.memory_use_cases import RetrieveMemoryUseCase, StoreMemoryUseCase
from tests.conftest import FakeEmbeddingGateway, FakeMemoryRepository


async def test_store_memory_embeds_and_persists(
    fake_embedding_gateway: FakeEmbeddingGateway, fake_memory_repository: FakeMemoryRepository
) -> None:
    use_case = StoreMemoryUseCase(fake_embedding_gateway, fake_memory_repository)
    user_id = uuid.uuid4()

    record = await use_case.execute(user_id, "the owner prefers morning meetings")

    assert record.user_id == user_id
    assert record.embedding is not None
    assert len(fake_memory_repository.records) == 1


async def test_retrieve_memory_only_returns_matching_user(
    fake_embedding_gateway: FakeEmbeddingGateway, fake_memory_repository: FakeMemoryRepository
) -> None:
    store = StoreMemoryUseCase(fake_embedding_gateway, fake_memory_repository)
    retrieve = RetrieveMemoryUseCase(fake_embedding_gateway, fake_memory_repository)
    user_a, user_b = uuid.uuid4(), uuid.uuid4()

    await store.execute(user_a, "fact about A")
    await store.execute(user_b, "fact about B")

    results = await retrieve.execute(user_a, "anything", top_k=5)

    assert len(results) == 1
    assert results[0].content == "fact about A"


async def test_retrieve_memory_respects_top_k(
    fake_embedding_gateway: FakeEmbeddingGateway, fake_memory_repository: FakeMemoryRepository
) -> None:
    store = StoreMemoryUseCase(fake_embedding_gateway, fake_memory_repository)
    retrieve = RetrieveMemoryUseCase(fake_embedding_gateway, fake_memory_repository)
    user_id = uuid.uuid4()

    for i in range(5):
        await store.execute(user_id, f"fact {i}")

    results = await retrieve.execute(user_id, "anything", top_k=2)
    assert len(results) == 2
