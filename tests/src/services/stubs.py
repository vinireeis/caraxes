from datetime import date

from src import ProjectModel, TaskModel, UserModel
from src.adapters.data_types.requests.projects_request import (
    NewProjectRequest,
    UpdateProjectRequest,
)
from src.adapters.data_types.requests.tasks_request import (
    NewTaskRequest,
    UpdateTaskRequest,
    UpdateTaskStatusRequest,
)
from src.adapters.data_types.requests.users_request import (
    NewUserRequest,
    UpdateUserRequest,
)
from src.adapters.data_types.typed_dicts.projects_typed_dict import (
    PaginatedProjectsTypedDict,
)
from src.adapters.data_types.typed_dicts.tasks_typed_dict import PaginatedTasksTypedDict
from src.adapters.data_types.typed_dicts.users_typed_dict import PaginatedUsersTypedDict
from src.domain.enums.projects.enum import ProjectStatusEnum
from src.domain.enums.tasks.enum import TaskStatusEnum, TaskPriorityEnum

user_model_stub = UserModel(
    id=10, name="John Doe", email="test@example.com", role="dev"
)

updated_user_model_stub = UserModel(
    id=10, name="Updated John Doe", email="updated@example.com", role="manager"
)

project_model_stub = ProjectModel(
    id=15, name="Test Project", status=ProjectStatusEnum.PLANNING
)

project_model_with_status_stub = ProjectModel(
    id=1, name="Project with Status", status=ProjectStatusEnum.CANCELLED
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

new_project_request_stub = NewProjectRequest(
    user_id=1,
    name="New Project",
    description="Test Project Description",
    status=ProjectStatusEnum.PLANNING,
    priority="HIGH",
    deadline="2025-12-31",
)

update_project_request_stub = UpdateProjectRequest(
    user_id=1,
    name="Updated Project",
    description="Updated Project Description",
    status=ProjectStatusEnum.ACTIVE,
    priority="MEDIUM",
    deadline="2025-01-31",
)

new_user_request_stub = NewUserRequest(
    name="New User", email="newuser@example.com", role="dev"
)

update_user_request_stub = UpdateUserRequest(
    name="Updated User", email="updateduser@example.com", role="manager"
)

new_task_request_stub = NewTaskRequest(
    name="New Task",
    description="New task description",
    status="TODO",
    priority="MEDIUM",
    deadline="2025-01-31",
    assigned_users=[1, 2],
)

update_task_request_stub = UpdateTaskRequest(
    name="Updated Task",
    description="Updated task description",
    status=TaskStatusEnum.IN_PROGRESS,
    priority=TaskPriorityEnum.LOW,
    deadline=date(2025, 3, 15),
)

update_task_status_request_stub = UpdateTaskStatusRequest(status=TaskStatusEnum.DONE)

paginated_tasks_stub: PaginatedTasksTypedDict = {
    "tasks": [task_model_stub],
    "total": 1,
    "limit": 10,
    "offset": 0,
}

paginated_projects_stub: PaginatedProjectsTypedDict = {
    "projects": [project_model_stub],
    "total": 1,
    "limit": 10,
    "offset": 0,
}

user_paginated_result_stub: PaginatedUsersTypedDict = {
    "users": [user_model_stub],
    "total": 1,
    "limit": 10,
    "offset": 0,
}
