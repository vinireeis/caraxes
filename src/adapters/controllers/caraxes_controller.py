from http import HTTPStatus

from src.adapters.data_types.requests.projects_request import (
    UpdateProjectRequest,
    NewProjectRequest,
)
from src.adapters.data_types.requests.tasks_request import (
    UpdateTaskStatusRequest,
    UpdateTaskRequest,
    NewTaskRequest,
)
from src.adapters.data_types.requests.users_request import (
    NewUserRequest,
    UpdateUserRequest,
)
from src.adapters.data_types.responses.projects_response import (
    DeleteProjectResponse,
    UpdateProjectResponse,
    ProjectsPaginatedPayload,
    ProjectsPaginatedResponse,
    ProjectPayload,
    GetOneProjectResponse,
    NewProjectResponse,
    ProjectIdPayload,
)
from src.adapters.data_types.responses.tasks_response import (
    DeleteTaskResponse,
    UpdateTaskStatusResponse,
    UpdateTaskResponse,
    TasksPaginatedPayload,
    TasksPaginatedResponse,
    TaskPayload,
    GetOneTaskResponse,
    NewTaskResponse,
    TaskIdPayload,
)
from src.adapters.data_types.responses.users_response import (
    NewUserResponse,
    UserIdPayload,
    GetOneUserResponse,
    UserPayload,
    UsersPaginatedResponse,
    UsersPaginatedPayload,
    UpdateUserResponse,
    DeleteUserResponse,
)
from src.services.projects.service import ProjectService
from src.services.tasks.service import TaskService
from src.services.users.service import UserService


class CaraxesController:

    _user_service: UserService = UserService()
    _project_service: ProjectService = ProjectService()
    _task_service: TaskService = TaskService()

    @classmethod
    async def create_new_user(cls, request: NewUserRequest) -> NewUserResponse:
        new_user_model = await UserService.create_new_user(
            request=request,
        )

        response = NewUserResponse(
            payload=UserIdPayload(id=new_user_model.id),
            sucess=True,
            message="User registered successfully.",
            status_code=HTTPStatus.CREATED,
        )

        return response

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> GetOneUserResponse:
        user_model = await UserService.get_user_by_id(user_id=user_id)

        get_one_user_response = GetOneUserResponse(
            payload=UserPayload(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                role=user_model.role if user_model.role else None,
            ),
            sucess=True,
            status_code=HTTPStatus.OK,
        )

        return get_one_user_response

    @classmethod
    async def get_users_paginated(
        cls, limit: int, offset: int
    ) -> UsersPaginatedResponse:
        users_paginated_result = await UserService.get_users_paginated(
            limit=limit, offset=offset
        )

        users_payload_list = [
            UserPayload(
                id=user.id,
                name=user.name,
                email=user.email,
                role=user.role if user.role else None,
            )
            for user in users_paginated_result.get("users", [])
        ]

        list_all_users_response = UsersPaginatedResponse(
            payload=UsersPaginatedPayload(
                users=users_payload_list,
                total=users_paginated_result.get("total"),
                limit=users_paginated_result.get("limit"),
                offset=users_paginated_result.get("offset"),
            ),
            sucess=True,
            status_code=HTTPStatus.OK,
        )

        return list_all_users_response

    @classmethod
    async def update_user_by_id(
        cls, user_id: int, request: UpdateUserRequest
    ) -> UpdateUserResponse:
        await UserService.update_user_by_id(user_id=user_id, request=request)

        update_user_response = UpdateUserResponse(
            success=True,
            message="User updated successfully.",
            status_code=HTTPStatus.OK,
        )

        return update_user_response

    @classmethod
    async def delete_user_by_id(cls, user_id: int) -> DeleteUserResponse:
        await UserService.delete_user_by_id(user_id=user_id)

        response = DeleteUserResponse(
            sucess=True,
            status_code=HTTPStatus.NO_CONTENT,
        )

        return response

    @classmethod
    async def create_new_project(cls, request: NewProjectRequest) -> NewProjectResponse:
        new_project_model = await ProjectService.create_new_project(request=request)
        response = NewProjectResponse(
            payload=ProjectIdPayload(id=new_project_model.id),
            success=True,
            message="Project created successfully.",
            status_code=HTTPStatus.CREATED,
        )
        return response

    @classmethod
    async def get_project_by_id(cls, project_id: int) -> GetOneProjectResponse:
        project_model = await ProjectService.get_project_by_id(project_id=project_id)
        response = GetOneProjectResponse(
            payload=ProjectPayload(
                id=project_model.id,
                user_id=project_model.user_id,
                name=project_model.name,
                description=project_model.description,
                status=project_model.status,
                start_date=project_model.start_date,
                end_date=project_model.end_date,
            ),
            success=True,
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def get_projects_paginated(
        cls, limit: int, offset: int
    ) -> ProjectsPaginatedResponse:
        projects_result = await ProjectService.get_projects_paginated(
            limit=limit, offset=offset
        )
        projects_payload_list = [
            ProjectPayload(
                id=project.id,
                user_id=project.user_id,
                name=project.name,
                description=project.description,
                status=project.status,
                start_date=project.start_date,
                end_date=project.end_date,
            )
            for project in projects_result.get("projects", [])
        ]
        response = ProjectsPaginatedResponse(
            payload=ProjectsPaginatedPayload(
                projects=projects_payload_list,
                total=projects_result.get("total"),
                limit=projects_result.get("limit"),
                offset=projects_result.get("offset"),
            ),
            success=True,
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def update_project(
        cls, project_id: int, request: UpdateProjectRequest
    ) -> UpdateProjectResponse:
        await ProjectService.update_project(project_id=project_id, request=request)
        response = UpdateProjectResponse(
            success=True,
            message="Project updated successfully.",
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def delete_project(cls, project_id: int) -> DeleteProjectResponse:
        await ProjectService.delete_project_by_id(project_id=project_id)
        response = DeleteProjectResponse(
            success=True,
            status_code=HTTPStatus.NO_CONTENT,
        )
        return response

    @classmethod
    async def create_new_task(
        cls, project_id: int, request: NewTaskRequest
    ) -> NewTaskResponse:
        new_task_model = await TaskService.create_new_task(
            project_id=project_id, request=request
        )
        response = NewTaskResponse(
            payload=TaskIdPayload(id=new_task_model.id),
            success=True,
            message="Task created successfully.",
            status_code=HTTPStatus.CREATED,
        )
        return response

    @classmethod
    async def get_task_by_id(cls, project_id: int, task_id: int) -> GetOneTaskResponse:
        task_model = await TaskService.get_task_by_id(
            project_id=project_id, task_id=task_id
        )
        response = GetOneTaskResponse(
            payload=TaskPayload(
                id=task_model.id,
                project_id=task_model.project_id,
                name=task_model.name,
                description=task_model.description,
                status=task_model.status,
                priority=task_model.priority,
                deadline=task_model.deadline,
                assigned_users=task_model.assigned_users,
                created_at=task_model.created_at,
                updated_at=task_model.updated_at,
            ),
            success=True,
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def get_tasks_paginated(
        cls,
        limit: int,
        offset: int,
        project_id: int | None = None,
        user_id: int | None = None,
    ) -> TasksPaginatedResponse:
        tasks_result = await TaskService.get_tasks_paginated(
            limit=limit, offset=offset, project_id=project_id, user_id=user_id
        )
        tasks_payload_list = [
            TaskPayload(
                id=task.id,
                project_id=task.project_id,
                name=task.name,
                description=task.description,
                status=task.status,
                priority=task.priority,
                deadline=task.deadline,
                assigned_users=task.assigned_users,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            for task in tasks_result.get("tasks", [])
        ]
        response = TasksPaginatedResponse(
            payload=TasksPaginatedPayload(
                tasks=tasks_payload_list,
                total=tasks_result.get("total"),
                limit=tasks_result.get("limit"),
                offset=tasks_result.get("offset"),
            ),
            success=True,
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def update_task(
        cls, project_id: int, task_id: int, request: UpdateTaskRequest
    ) -> UpdateTaskResponse:
        await TaskService.update_task(
            project_id=project_id, task_id=task_id, request=request
        )
        response = UpdateTaskResponse(
            success=True,
            message="Task updated successfully.",
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def update_task_status(
        cls, project_id: int, task_id: int, request: UpdateTaskStatusRequest
    ) -> UpdateTaskStatusResponse:
        await TaskService.update_task_status(
            project_id=project_id, task_id=task_id, request=request
        )
        response = UpdateTaskStatusResponse(
            success=True,
            message="Task status updated successfully.",
            status_code=HTTPStatus.OK,
        )
        return response

    @classmethod
    async def delete_task(cls, project_id: int, task_id: int) -> DeleteTaskResponse:
        await TaskService.delete_task(project_id=project_id, task_id=task_id)
        response = DeleteTaskResponse(
            success=True,
            status_code=HTTPStatus.NO_CONTENT,
        )
        return response
