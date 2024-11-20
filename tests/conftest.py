from unittest.mock import patch, AsyncMock

import pytest


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

        yield mock_project_repository


@pytest.fixture
def mock_user_service():
    with patch(
        "src.services.projects.service.ProjectService._user_service"
    ) as mock_user_service:
        mock_user_service.get_user_by_id = AsyncMock()
        yield mock_user_service


@pytest.fixture
def mock_user_exists():
    with patch(
        "src.services.projects.service.ProjectService._user_service"
    ) as mock_user_exists:
        mock_user_exists.get_user_by_id = AsyncMock()
        yield mock_user_exists
