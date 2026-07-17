from __future__ import annotations

from fastapi.testclient import TestClient


def test_liveness_returns_ok(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_ui_root_serves_html(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Edith" in response.text
