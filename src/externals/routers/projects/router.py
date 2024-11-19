from decouple import config
from fastapi import APIRouter, Query

from src.adapters.controllers.caraxes_controller import CaraxesController
from src.domain.enums.projects.enum import ProjectStatusEnum
from src.adapters.data_types.requests.projects_request import (
    NewProjectRequest,
    UpdateProjectRequest,
)
from src.adapters.data_types.responses.projects_response import (
    ProjectsPaginatedResponse,
    GetOneProjectResponse,
    NewProjectResponse,
    DeleteProjectResponse,
    UpdateProjectResponse,
)


class ProjectsRouter:
    __router = APIRouter(prefix=config("ROOT_PATH"), tags=["Projects"])

    @staticmethod
    def get_projects_router():
        return ProjectsRouter.__router

    @staticmethod
    @__router.post(
        path="/projects",
        response_model=NewProjectResponse,
        response_model_exclude_none=True,
    )
    async def create_new_project(request: NewProjectRequest) -> NewProjectResponse:
        response = await CaraxesController.create_new_project(request=request)
        return response

    @staticmethod
    @__router.get(
        path="/projects",
        response_model=ProjectsPaginatedResponse,
        response_model_exclude_none=True,
    )
    async def get_projects_paginated(
        limit: int = Query(default=10, ge=1),
        offset: int = Query(default=0, ge=0),
        status: ProjectStatusEnum | None = Query(default=None),
        user_id: int | None = Query(default=None),
    ) -> ProjectsPaginatedResponse:
        response = await CaraxesController.get_projects_paginated(
            limit=limit, offset=offset, status=status, user_id=user_id
        )
        return response

    @staticmethod
    @__router.get(
        path="/projects/{project_id}",
        response_model=GetOneProjectResponse,
        response_model_exclude_none=True,
    )
    async def get_one_project(project_id: int) -> GetOneProjectResponse:
        response = await CaraxesController.get_project_by_id(project_id=project_id)
        return response

    @staticmethod
    @__router.put(
        path="/projects/{project_id}",
        response_model=UpdateProjectResponse,
        response_model_exclude_none=True,
    )
    async def update_project(
        project_id: int, request: UpdateProjectRequest
    ) -> UpdateProjectResponse:
        response = await CaraxesController.update_project(
            project_id=project_id, request=request
        )
        return response

    @staticmethod
    @__router.delete(
        path="/projects/{project_id}",
        response_model=DeleteProjectResponse,
        response_model_exclude_none=True,
    )
    async def delete_project(project_id: int) -> DeleteProjectResponse:
        response = await CaraxesController.delete_project(project_id=project_id)
        return response
