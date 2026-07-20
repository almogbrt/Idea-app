from __future__ import annotations

import uuid
from abc import ABC, abstractmethod

from app.domain.entities import Project, ProjectStatus, ProjectSummary


class ProjectRepositoryPort(ABC):
    @abstractmethod
    async def create(
        self,
        user_id: uuid.UUID,
        name: str,
        client_id: uuid.UUID | None = None,
        status: ProjectStatus = ProjectStatus.IN_PROGRESS,
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
    async def update_status(self, project_id: uuid.UUID, status: ProjectStatus) -> Project:
        raise NotImplementedError

    @abstractmethod
    async def count_active(self, user_id: uuid.UUID) -> int:
        raise NotImplementedError

    @abstractmethod
    async def assign_client(self, project_id: uuid.UUID, client_id: uuid.UUID) -> Project:
        raise NotImplementedError
