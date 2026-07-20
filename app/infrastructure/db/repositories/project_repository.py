from __future__ import annotations

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.ports.project_repository import ProjectRepositoryPort
from app.core.exceptions import NotFoundError
from app.domain.entities import Project, ProjectStatus, ProjectSummary
from app.infrastructure.db.models import ClientModel, ProjectModel, TaskModel


class SqlAlchemyProjectRepository(ProjectRepositoryPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        user_id: uuid.UUID,
        name: str,
        client_id: uuid.UUID | None = None,
        status: ProjectStatus = ProjectStatus.IN_PROGRESS,
    ) -> Project:
        row = ProjectModel(user_id=user_id, name=name, client_id=client_id, status=status.value)
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def list_by_user(self, user_id: uuid.UUID) -> list[ProjectSummary]:
        stmt = (
            select(ProjectModel, ClientModel.name)
            .outerjoin(ClientModel, ProjectModel.client_id == ClientModel.id)
            .where(ProjectModel.user_id == user_id)
            .order_by(ProjectModel.updated_at.desc())
        )
        rows = (await self._session.execute(stmt)).all()
        projects = [row[0] for row in rows]
        client_names = {row[0].id: row[1] for row in rows}

        last_tasks: dict[uuid.UUID, str] = {}
        project_ids = [p.id for p in projects]
        if project_ids:
            task_stmt = (
                select(TaskModel.project_id, TaskModel.title)
                .distinct(TaskModel.project_id)
                .where(TaskModel.project_id.in_(project_ids))
                .order_by(TaskModel.project_id, TaskModel.updated_at.desc())
            )
            task_rows = (await self._session.execute(task_stmt)).all()
            last_tasks = {row[0]: row[1] for row in task_rows}

        return [
            ProjectSummary(
                project=self._to_entity(p),
                client_name=client_names.get(p.id),
                last_task_title=last_tasks.get(p.id),
            )
            for p in projects
        ]

    async def get(self, project_id: uuid.UUID) -> Project | None:
        row = await self._session.get(ProjectModel, project_id)
        return self._to_entity(row) if row else None

    async def get_summary(self, project_id: uuid.UUID) -> ProjectSummary | None:
        stmt = (
            select(ProjectModel, ClientModel.name)
            .outerjoin(ClientModel, ProjectModel.client_id == ClientModel.id)
            .where(ProjectModel.id == project_id)
        )
        row = (await self._session.execute(stmt)).first()
        if row is None:
            return None
        project_row, client_name = row

        last_task_stmt = (
            select(TaskModel.title)
            .where(TaskModel.project_id == project_id)
            .order_by(TaskModel.updated_at.desc())
            .limit(1)
        )
        last_task_title = (await self._session.execute(last_task_stmt)).scalar_one_or_none()

        return ProjectSummary(
            project=self._to_entity(project_row),
            client_name=client_name,
            last_task_title=last_task_title,
        )

    async def update_status(self, project_id: uuid.UUID, status: ProjectStatus) -> Project:
        row = await self._session.get(ProjectModel, project_id)
        if row is None:
            raise NotFoundError("Project not found", details={"project_id": str(project_id)})
        row.status = status.value
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def assign_client(self, project_id: uuid.UUID, client_id: uuid.UUID) -> Project:
        row = await self._session.get(ProjectModel, project_id)
        if row is None:
            raise NotFoundError("Project not found", details={"project_id": str(project_id)})
        row.client_id = client_id
        await self._session.flush()
        await self._session.refresh(row)
        return self._to_entity(row)

    async def delete(self, project_id: uuid.UUID) -> None:
        row = await self._session.get(ProjectModel, project_id)
        if row is None:
            raise NotFoundError("Project not found", details={"project_id": str(project_id)})
        await self._session.delete(row)
        await self._session.flush()

    async def count_active(self, user_id: uuid.UUID) -> int:
        stmt = (
            select(func.count())
            .select_from(ProjectModel)
            .where(
                ProjectModel.user_id == user_id,
                ProjectModel.status == ProjectStatus.IN_PROGRESS.value,
            )
        )
        return (await self._session.execute(stmt)).scalar_one()

    @staticmethod
    def _to_entity(row: ProjectModel) -> Project:
        return Project(
            id=row.id,
            user_id=row.user_id,
            client_id=row.client_id,
            name=row.name,
            status=ProjectStatus(row.status),
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
