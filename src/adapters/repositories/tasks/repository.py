from loguru import logger
from sqlalchemy import select, func, insert, delete
from sqlalchemy.exc import NoResultFound

from src import TaskModel
from src.adapters.data_types.requests.tasks_request import (
    NewTaskRequest,
    UpdateTaskRequest,
)
from src.adapters.data_types.typed_dicts.tasks_typed_dict import PaginatedTasksTypedDict
from src.domain.enums.tasks.enum import TaskStatusEnum
from src.domain.exceptions.repository.exception import TaskNotFoundError
from src.externals.infrastructures.postgres.infrastructure import PostgresInfrastructure


class TaskRepository:
    postgres_infrastructure = PostgresInfrastructure()

    @classmethod
    async def insert_one_task(
        cls, project_id: int, task_request: NewTaskRequest
    ) -> TaskModel:
        async with cls.postgres_infrastructure.get_session() as session:
            task_dict = task_request.model_dump()
            task_dict["project_id"] = project_id

            statement = insert(TaskModel).values(task_dict).returning(TaskModel)
            db_result = await session.execute(statement)
            await session.commit()

            new_task_model = db_result.fetchone()
            return new_task_model

    @classmethod
    async def get_tasks_paginated(
        cls,
        limit: int,
        offset: int,
        project_id: int | None = None,
        user_id: int | None = None,
    ) -> PaginatedTasksTypedDict:
        async with cls.postgres_infrastructure.get_session() as session:
            query = select(TaskModel)

            if project_id:
                query = query.where(TaskModel.project_id == project_id)
            if user_id:
                query = query.join(TaskModel.assigned_users).where(
                    TaskModel.assigned_users.any(id=user_id)
                )

            query = query.limit(limit).offset(offset)
            db_result = await session.execute(query)
            tasks_model = db_result.scalars().all()

            total_tasks = await session.execute(select(func.count(TaskModel.id)))
            total_count = total_tasks.scalar()

            return PaginatedTasksTypedDict(
                tasks=tasks_model, total=total_count, limit=limit, offset=offset
            )

    async def get_one_task_by_id(self, project_id: int, task_id: int) -> TaskModel:
        async with self.postgres_infrastructure.get_session() as session:
            statement = select(TaskModel).where(
                TaskModel.project_id == project_id, TaskModel.id == task_id
            )
            try:
                db_result = await session.execute(statement)
                task = db_result.scalar_one()
                return task
            except NoResultFound as ex:
                logger.info(ex)
                raise TaskNotFoundError(task_id)

    async def update_task(
        self, project_id: int, task_id: int, task_request: UpdateTaskRequest
    ) -> TaskModel:
        async with self.postgres_infrastructure.get_session() as session:
            statement = select(TaskModel).where(
                TaskModel.project_id == project_id, TaskModel.id == task_id
            )
            try:
                db_result = await session.execute(statement)
                task = db_result.scalar_one()

                task_data = task_request.model_dump(exclude_unset=True)
                for key, value in task_data.items():
                    setattr(task, key, value)

                await session.commit()
                return task
            except NoResultFound as ex:
                logger.info(ex)
                raise TaskNotFoundError(task_id)

    async def update_task_status(
        self, project_id: int, task_id: int, status: TaskStatusEnum
    ) -> TaskModel:
        async with self.postgres_infrastructure.get_session() as session:
            statement = select(TaskModel).where(
                TaskModel.project_id == project_id, TaskModel.id == task_id
            )
            try:
                db_result = await session.execute(statement)
                task = db_result.scalar_one()

                task.status = status
                await session.commit()
                return task
            except NoResultFound as ex:
                logger.info(ex)
                raise TaskNotFoundError(task_id)

    async def delete_one_task_by_id(self, project_id: int, task_id: int) -> None:
        async with self.postgres_infrastructure.get_session() as session:
            statement = (
                delete(TaskModel)
                .where(TaskModel.project_id == project_id, TaskModel.id == task_id)
                .returning(TaskModel.id)
            )

            db_result = await session.execute(statement)
            deleted_id = db_result.scalar()

            if not deleted_id:
                raise TaskNotFoundError(task_id=task_id)

            await session.commit()
