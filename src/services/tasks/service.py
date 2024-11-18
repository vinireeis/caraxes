from asyncio import gather

from src import TaskModel
from src.adapters.data_types.requests.tasks_request import (
    NewTaskRequest,
    UpdateTaskRequest,
    UpdateTaskStatusRequest,
)
from src.adapters.data_types.typed_dicts.tasks_typed_dict import PaginatedTasksTypedDict
from src.adapters.repositories.tasks.repository import TaskRepository
from src.domain.enums.projects.enum import ProjectStatusEnum
from src.domain.exceptions.repository.exception import UserNotFoundError
from src.domain.exceptions.service.exception import (
    InvalidProjectStatusForTaskCreationError,
    InvalidAssignedUserError,
)
from src.services.projects.service import ProjectService
from src.services.users.service import UserService


class TaskService:
    _task_repository: TaskRepository = TaskRepository()
    _project_service: ProjectService = ProjectService()
    _user_service: UserService = UserService()

    @classmethod
    async def create_new_task(
        cls, project_id: int, request: NewTaskRequest
    ) -> TaskModel:
        await cls.validate_project_status_is_planning_or_active(project_id=project_id)
        await cls.validate_users_assigned_ids_already_exists(request=request)

        new_task_model = await cls._task_repository.insert_one_task(
            project_id=project_id, task_request=request
        )

        return new_task_model

    @classmethod
    async def get_tasks_paginated(
        cls,
        limit: int,
        offset: int,
        project_id: int | None = None,
        user_id: int | None = None,
    ) -> PaginatedTasksTypedDict:
        tasks_paginated_result = await cls._task_repository.get_tasks_paginated(
            limit=limit, offset=offset, project_id=project_id, user_id=user_id
        )

        return tasks_paginated_result

    @classmethod
    async def get_task_by_id(cls, project_id: int, task_id: int) -> TaskModel:
        task_model = await cls._task_repository.get_one_task_by_id(
            project_id=project_id, task_id=task_id
        )

        return task_model

    @classmethod
    async def update_task(
        cls,
        project_id: int,
        task_id: int,
        request: UpdateTaskRequest,
    ):
        await cls.validate_project_status_is_planning_or_active(project_id=project_id)
        await cls.validate_users_assigned_ids_already_exists(request=request)

        await cls._task_repository.update_task(
            project_id=project_id, task_id=task_id, task_request=request
        )

    @classmethod
    async def update_task_status(
        cls,
        project_id: int,
        task_id: int,
        request: UpdateTaskStatusRequest,
    ):
        await cls.validate_project_status_is_planning_or_active(project_id=project_id)

        await cls._task_repository.update_task_status(
            project_id=project_id, task_id=task_id, status=request.status
        )

    @classmethod
    async def delete_task(
        cls,
        project_id: int,
        task_id: int,
    ):
        await cls._task_repository.delete_one_task_by_id(
            project_id=project_id, task_id=task_id
        )

    @classmethod
    async def validate_project_status_is_planning_or_active(cls, project_id: int):

        project_model = await cls._project_service.get_project_by_id(
            project_id=project_id
        )

        if project_model.status in [
            ProjectStatusEnum.CANCELLED,
            ProjectStatusEnum.PAUSED,
            ProjectStatusEnum.COMPLETED,
        ]:
            raise InvalidProjectStatusForTaskCreationError()

    @classmethod
    async def validate_users_assigned_ids_already_exists(
        cls, request: NewTaskRequest | UpdateTaskRequest
    ):
        try:
            tasks = [
                cls._user_service.get_user_by_id(user_id=user_id)
                for user_id in request.assigned_user_ids
            ]

            await gather(*tasks)

        except UserNotFoundError:
            raise InvalidAssignedUserError()
