from datetime import datetime

from pydantic import BaseModel, Field

from src.adapters.data_types.responses.base.base_response import BaseResponse
from src.domain.enums.projects.enum import ProjectStatusEnum


class ProjectPayload(BaseModel):
    id: int
    user_id: int
    name: str
    status: ProjectStatusEnum
    description: str | None
    start_date: datetime | None
    end_date: datetime | None


class ProjectsPaginatedPayload(BaseModel):
    projects: list[ProjectPayload] = Field(default_factory=list)
    total: int
    limit: int
    offset: int


class ProjectIdPayload(BaseModel):
    id: int


class ProjectsPaginatedResponse(BaseResponse):
    payload: ProjectsPaginatedPayload


class GetOneProjectResponse(BaseResponse):
    payload: ProjectPayload


class NewProjectResponse(BaseResponse):
    payload: ProjectIdPayload


class UpdateProjectResponse(BaseResponse):
    pass


class DeleteProjectResponse(BaseResponse):
    pass
