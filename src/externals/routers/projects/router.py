from typing import Annotated
from decouple import config
from fastapi import APIRouter, Query
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
from src.services.projects.service import ProjectService


class ProjectsRouter:
    __router = APIRouter(prefix=config("ROOT_PATH"), tags=["Projects"])

    @staticmethod
    def get_projects_router():
        return ProjectsRouter.__router

    @staticmethod
    @__router.post(path="/projects", response_model=NewProjectResponse)
    async def create_new_project(request: NewProjectRequest) -> NewProjectResponse:
        response = await ProjectService.create_new_project(request=request)
        return response

    @staticmethod
    @__router.get(path="/projects", response_model=ProjectsPaginatedResponse)
    async def get_projects_paginated(
        limit: Annotated[int, Query(default=10, ge=1)],
        offset: Annotated[int, Query(default=0, ge=0)],
        status: Annotated[ProjectStatusEnum | None, Query(default=None)],
        user_id: Annotated[int | None, Query(default=None)],
    ) -> ProjectsPaginatedResponse:
        response = await ProjectService.get_projects_paginated(
            limit=limit, offset=offset, status=status, user_id=user_id
        )
        return response

    @staticmethod
    @__router.get(path="/projects/{project_id}", response_model=GetOneProjectResponse)
    async def get_one_project(project_id: int) -> GetOneProjectResponse:
        response = await ProjectService.get_project_by_id(project_id=project_id)
        return response

    @staticmethod
    @__router.put(path="/projects/{project_id}", response_model=UpdateProjectResponse)
    async def update_project(
        project_id: int, request: UpdateProjectRequest
    ) -> UpdateProjectResponse:
        response = await ProjectService.update_project(
            project_id=project_id, request=request
        )
        return response

    @staticmethod
    @__router.delete(
        path="/projects/{project_id}", response_model=DeleteProjectResponse
    )
    async def delete_project(project_id: int) -> DeleteProjectResponse:
        response = await ProjectService.delete_project_by_id(project_id=project_id)
        return response
