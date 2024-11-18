from src import ProjectModel
from src.adapters.data_types.requests.projects_request import (
    NewProjectRequest,
    UpdateProjectRequest,
)
from src.adapters.data_types.typed_dicts.projects_typed_dict import (
    PaginatedProjectsTypedDict,
)
from src.adapters.repositories.projects.repository import ProjectRepository
from src.domain.enums.projects.enum import ProjectStatusEnum
from src.services.users.service import UserService


class ProjectService:
    _project_repository: ProjectRepository = ProjectRepository()
    _user_service: UserService = UserService()

    @classmethod
    async def create_new_project(cls, request: NewProjectRequest) -> ProjectModel:
        await cls.verify_user_exists(user_id=request.user.id)

        new_project_model = await cls._project_repository.insert_one_project(
            project_request=request
        )

        return new_project_model

    @classmethod
    async def get_project_by_id(cls, project_id: int) -> ProjectModel:
        project_model = await cls._project_repository.get_one_project_by_id(
            project_id=project_id
        )

        return project_model

    @classmethod
    async def get_projects_paginated(
        cls,
        limit: int,
        offset: int,
        status: ProjectStatusEnum | None = None,
        user_id: int | None = None,
    ) -> PaginatedProjectsTypedDict:
        projects_paginated_result = (
            await cls._project_repository.get_projects_paginated(
                limit=limit, offset=offset, status=status, user_id=user_id
            )
        )

        return projects_paginated_result

    @classmethod
    async def update_project(cls, project_id: int, request: UpdateProjectRequest):
        await cls.verify_user_exists(user_id=request.user.id)
        await cls._project_repository.update_project(
            project_id=project_id, project_request=request
        )

    @classmethod
    async def delete_project_by_id(cls, project_id: int):
        await cls._project_repository.delete_one_project_by_id(project_id=project_id)

    @classmethod
    async def verify_user_exists(cls, user_id: int):
        await cls._user_service.get_user_by_id(user_id=user_id)
