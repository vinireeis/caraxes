from typing import Annotated
from decouple import config
from fastapi import APIRouter, Query

from src.adapters.controllers.caraxes_controller import CaraxesController
from src.adapters.data_types.requests.tasks_request import (
    NewTaskRequest,
    UpdateTaskRequest,
    UpdateTaskStatusRequest,
)
from src.adapters.data_types.responses.tasks_response import (
    TasksPaginatedResponse,
    GetOneTaskResponse,
    NewTaskResponse,
    DeleteTaskResponse,
    UpdateTaskResponse,
    UpdateTaskStatusResponse,
)


class TasksRouter:
    __router = APIRouter(prefix=config("ROOT_PATH"), tags=["Tasks"])

    @staticmethod
    def get_tasks_router():
        return TasksRouter.__router

    @staticmethod
    @__router.get(path="/projects/tasks", response_model=TasksPaginatedResponse)
    async def get_tasks_paginated(
        limit: Annotated[int, Query(default=10, ge=1)],
        offset: Annotated[int, Query(default=0, ge=0)],
        project_id: Annotated[int | None, Query(default=None)],
        user_id: Annotated[int | None, Query(default=None)],
    ) -> TasksPaginatedResponse:
        response = await CaraxesController.get_tasks_paginated(
            limit=limit, offset=offset, project_id=project_id, user_id=user_id
        )

        return response

    @staticmethod
    @__router.get(
        path="/projects/{project_id}/tasks/{task_id}", response_model=GetOneTaskResponse
    )
    async def get_one_task(project_id: int, task_id: int) -> GetOneTaskResponse:
        response = await CaraxesController.get_task_by_id(
            project_id=project_id, task_id=task_id
        )

        return response

    @staticmethod
    @__router.post(path="/projects/{project_id}/tasks", response_model=NewTaskResponse)
    async def create_new_task(
        project_id: int, request: NewTaskRequest
    ) -> NewTaskResponse:
        response = await CaraxesController.create_new_task(
            project_id=project_id, request=request
        )

        return response

    @staticmethod
    @__router.put(
        path="/projects/{project_id}/tasks/{task_id}", response_model=UpdateTaskResponse
    )
    async def update_task(
        project_id: int, task_id: int, request: UpdateTaskRequest
    ) -> UpdateTaskResponse:
        response = await CaraxesController.update_task(
            project_id=project_id, task_id=task_id, request=request
        )

        return response

    @staticmethod
    @__router.patch(
        path="/projects/{project_id}/tasks/{task_id}/status",
        response_model=UpdateTaskStatusResponse,
    )
    async def update_task_status(
        project_id: int, task_id: int, request: UpdateTaskStatusRequest
    ) -> UpdateTaskStatusResponse:
        response = await CaraxesController.update_task_status(
            project_id=project_id, task_id=task_id, request=request
        )

        return response

    @staticmethod
    @__router.delete(
        path="/projects/{project_id}/tasks/{task_id}", response_model=DeleteTaskResponse
    )
    async def delete_task(project_id: int, task_id: int) -> DeleteTaskResponse:
        response = await CaraxesController.delete_task(
            project_id=project_id, task_id=task_id
        )

        return response
