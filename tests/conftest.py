from unittest.mock import patch, AsyncMock

import pytest

from src import ProjectModel
from tests.src.services.stubs import (
    task_model_stub,
    paginated_tasks_stub,
)


@pytest.fixture
def mock_task_repository():
    with patch(
        "src.services.tasks.service.TaskService._task_repository"
    ) as mock_task_repo:
        mock_task_repo.insert_one_task = AsyncMock(return_value=task_model_stub)
        mock_task_repo.get_tasks_paginated = AsyncMock(
            return_value=paginated_tasks_stub
        )
        mock_task_repo.get_one_task_by_id = AsyncMock(return_value=task_model_stub)
        mock_task_repo.update_task = AsyncMock()
        mock_task_repo.update_task_status = AsyncMock()
        mock_task_repo.delete_one_task_by_id = AsyncMock()
        yield mock_task_repo


@pytest.fixture
def mock_project_repository():
    with patch(
        "src.services.projects.service.ProjectService._project_repository"
    ) as mock_project_repository:
        mock_project_repository.delete_one_project_by_id = AsyncMock()
        mock_project_repository.insert_one_project = AsyncMock()
        mock_project_repository.update_project = AsyncMock()
        mock_project_repository.get_one_project_by_id = AsyncMock()
        mock_project_repository.get_projects_paginated = AsyncMock()
        mock_project_repository.get_one_project_by_id.return_value = ProjectModel(
            id=15, name="Test Project"
        )

        yield mock_project_repository


@pytest.fixture
def mock_user_service():
    with patch(
        "src.services.projects.service.ProjectService._user_service"
    ) as mock_user_service:
        mock_user_service.get_user_by_id = AsyncMock()
        yield mock_user_service
