from datetime import date

from src.adapters.data_types.requests.tasks_request import (
    UpdateTaskRequest,
    NewTaskRequest,
)
from src.adapters.data_types.typed_dicts.tasks_typed_dict import PaginatedTasksTypedDict
from src import ProjectModel, UserModel, TaskModel
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

project_model_with_status_stub = ProjectModel(
    id=1, name="Test Project", status=ProjectStatusEnum.CANCELLED
)

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

task_model_stub = TaskModel(
    id=1,
    project_id=15,
    name="Task 1",
    description="Test task description",
    status="TODO",
    priority="HIGH",
    deadline=date.fromisoformat("2024-12-31"),
)

new_task_request_stub = NewTaskRequest(
    name="New Task",
    description="New task description",
    status="TODO",
    priority="HIGH",
    deadline="2024-12-31",
    assigned_users=[1, 2],  # Assigning users with IDs
)

update_task_request_stub = UpdateTaskRequest(
    name="Updated Task",
    description="Updated task description",
    status="IN_PROGRESS",
    priority="MEDIUM",
    deadline="2025-01-31",
    assigned_users=[1],
)

paginated_tasks_stub = PaginatedTasksTypedDict(
    tasks=[task_model_stub], total=1, limit=10, offset=0
)

paginated_tasks_typed_dict_stub = PaginatedTasksTypedDict(
    tasks=[task_model_stub], total=1, limit=10, offset=0
)
