from src import ProjectModel, UserModel
from src.adapters.data_types.typed_dicts.users_typed_dict import PaginatedUsersTypedDict
from src.adapters.data_types.requests.projects_request import (
    NewProjectRequest,
    UpdateProjectRequest,
)
from src.adapters.data_types.requests.users_request import (
    NewUserRequest,
    UpdateUserRequest,
)
from src.adapters.data_types.typed_dicts.projects_typed_dict import (
    PaginatedProjectsTypedDict,
)
from src.domain.enums.projects.enum import ProjectStatusEnum

user_model_stub = UserModel(
    id=10, name="John Doe", email="test@example.com", role="dev"
)

project_model_stub = ProjectModel(id=15, name="Test Project")

new_user_request_stub = NewUserRequest(
    name="Test User", email="test@example.com", role="dev"
)

update_user_request_stub = UpdateUserRequest(
    name="Updated User", email="updated@example.com", role="manager"
)

updated_user_model_stub = UserModel(
    id=10, name="Updated User", email="updated@example.com", role="manager"
)

user_paginated_result_stub = PaginatedUsersTypedDict(
    users=[user_model_stub], total=1, limit=10, offset=0
)

new_project_request_stub = NewProjectRequest(
    user_id=1,
    name="New Project",
    description="Test description",
    status=ProjectStatusEnum.PLANNING,
    priority="HIGH",
    deadline="2024-12-31",
)

update_project_request_stub = UpdateProjectRequest(
    user_id=1,
    name="Updated Project",
    description="Updated description",
    status=ProjectStatusEnum.PLANNING,
    priority="HIGH",
    deadline="2024-12-31",
)

paginated_projects_stub = PaginatedProjectsTypedDict(
    projects=[ProjectModel(id=1, name="Test Project")], total=1, limit=10, offset=0
)
