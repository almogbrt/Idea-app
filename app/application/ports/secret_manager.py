from __future__ import annotations

from abc import ABC, abstractmethod


class SecretManagerPort(ABC):
    """Abstracts secret retrieval so `env` (local) and `gcp` (Secret Manager)
    backends are interchangeable behind one interface."""

    @abstractmethod
    def get_secret(self, name: str) -> str:
        raise NotImplementedError
