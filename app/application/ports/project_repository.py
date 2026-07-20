from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import Project, ProjectSummary, ProjectType


class ProjectRepositoryPort(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: uuid.UUID,
        name: str,
        client_id: uuid.UUID | None,
        type: ProjectType,
    ) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def list_by_user(self, user_id: uuid.UUID) -> list[ProjectSummary]:
        """Ordered by most recently updated first, with client name and the
        project's most recent task title denormalized in for the dashboard."""
        raise NotImplementedError

    @abstractmethod
    async def get(self, project_id: uuid.UUID) -> Project | None:
        raise NotImplementedError

    @abstractmethod
    async def get_summary(self, project_id: uuid.UUID) -> ProjectSummary | None:
        raise NotImplementedError

    @abstractmethod
    async def update_type(self, project_id: uuid.UUID, type: ProjectType) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def count_active(self, user_id: uuid.UUID) -> int:
        """Total number of projects for this user (kept as a headline count
        for the dashboard now that projects no longer have a status)."""
        raise NotImplementedError

    @abstractmethod
    async def assign_client(self, project_id: uuid.UUID, client_id: uuid.UUID) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, project_id: uuid.UUID) -> None:
        raise NotImplementedError
