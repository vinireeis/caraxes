from loguru import logger
from sqlalchemy import select, func, insert, delete
from sqlalchemy.exc import NoResultFound

from src import ProjectModel
from src.adapters.data_types.requests.projects_request import (
    NewProjectRequest,
    UpdateProjectRequest,
)
from src.adapters.data_types.typed_dicts.projects_typed_dict import (
    PaginatedProjectsTypedDict,
)
from src.domain.exceptions.repository.exception import ProjectNotFoundError
from src.externals.infrastructures.postgres.infrastructure import PostgresInfrastructure


class ProjectRepository:
    postgres_infrastructure = PostgresInfrastructure()

    @classmethod
    async def insert_one_project(
        cls, project_request: NewProjectRequest
    ) -> ProjectModel:
        async with cls.postgres_infrastructure.get_session() as session:
            project_dict = project_request.model_dump()
            statement = (
                insert(ProjectModel).values(project_dict).returning(ProjectModel)
            )
            db_result = await session.execute(statement)

            await session.commit()
            new_project_model = db_result.fetchone()

            return new_project_model

    @classmethod
    async def get_projects_paginated(
        cls, limit=10, offset=0, status=None, user_id=None
    ) -> PaginatedProjectsTypedDict:
        async with cls.postgres_infrastructure.get_session() as session:
            query = select(ProjectModel)

            if user_id:
                query = query.where(ProjectModel.user_id == user_id)
            if status:
                query = query.where(ProjectModel.status == status)

            query = query.limit(limit).offset(offset)
            db_result = await session.execute(query)
            projects_model = db_result.scalars().all()

            total_projects = await session.execute(select(func.count(ProjectModel.id)))
            total_count = total_projects.scalar()

            return PaginatedProjectsTypedDict(
                projects=projects_model, total=total_count, limit=limit, offset=offset
            )

    async def get_one_project_by_id(self, project_id: int) -> ProjectModel:
        async with self.postgres_infrastructure.get_session() as session:
            statement = select(ProjectModel).where(ProjectModel.id == project_id)
            try:
                db_result = await session.execute(statement)
                project = db_result.scalar_one()
                return project

            except NoResultFound as ex:
                logger.info(ex)
                raise ProjectNotFoundError(project_id)

    async def update_project(
        self, project_id: int, project_request: UpdateProjectRequest
    ) -> ProjectModel:
        async with self.postgres_infrastructure.get_session() as session:
            statement = select(ProjectModel).where(ProjectModel.id == project_id)
            try:
                db_result = await session.execute(statement)
                project = db_result.scalar_one()

                project_data = project_request.model_dump(exclude_unset=True)
                for key, value in project_data.items():
                    setattr(project, key, value)

                await session.commit()
                return project

            except NoResultFound as ex:
                logger.info(ex)
                raise ProjectNotFoundError(project_id)

    async def delete_one_project_by_id(self, project_id: int) -> None:
        async with self.postgres_infrastructure.get_session() as session:
            statement = (
                delete(ProjectModel)
                .where(ProjectModel.id == project_id)
                .returning(ProjectModel.id)
            )

            db_result = await session.execute(statement)
            deleted_id = db_result.scalar()

            if not deleted_id:
                raise ProjectNotFoundError(project_id=project_id)

            await session.commit()
