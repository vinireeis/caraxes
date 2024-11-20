import pytest

from src.services.projects.service import ProjectService
from src.domain.models.projects.model import ProjectModel
from tests.src.services.stubs import (
    project_model_stub,
    user_model_stub,
    new_project_request_stub,
    paginated_projects_stub,
    update_project_request_stub,
)


@pytest.mark.asyncio
async def test_when_create_new_project_then_return_project_model(
    mock_project_repository, mock_user_service
):

    mock_user_service.get_user_by_id.return_value = user_model_stub
    mock_project_repository.insert_one_project.return_value = project_model_stub
    new_project_model = await ProjectService.create_new_project(
        request=new_project_request_stub
    )
    mock_project_repository.insert_one_project.assert_called_once_with(
        project_request=new_project_request_stub
    )

    assert isinstance(new_project_model, ProjectModel)
    assert new_project_model.id == project_model_stub.id
    assert new_project_model.name == "Test Project"


@pytest.mark.asyncio
async def test_when_get_project_by_id_then_return_project_model(
    mock_project_repository,
):
    project_id = 15
    mock_project_repository.get_one_project_by_id.return_value = project_model_stub

    project_model_returned = await ProjectService.get_project_by_id(
        project_id=project_id
    )

    mock_project_repository.get_one_project_by_id.assert_called_once_with(
        project_id=project_id
    )
    assert isinstance(project_model_returned, ProjectModel)
    assert project_model_returned.id == project_model_stub.id
    assert project_model_returned.name == "Test Project"


@pytest.mark.asyncio
async def test_when_get_projects_paginated_then_return_paginated_projects_typed_dict(
    mock_project_repository,
):
    limit = 10
    offset = 0
    mock_project_repository.get_projects_paginated.return_value = (
        paginated_projects_stub
    )

    paginated_result = await ProjectService.get_projects_paginated(
        limit=limit, offset=offset
    )

    mock_project_repository.get_projects_paginated.assert_called_once_with(
        limit=limit, offset=offset, status=None, user_id=None
    )
    assert len(paginated_result["projects"]) == 1
    assert paginated_result["total"] == 1
    assert paginated_result["limit"] == 10
    assert paginated_result["offset"] == 0


@pytest.mark.asyncio
async def test_when_update_project_then_repository_is_called_with_correct_arguments(
    mock_project_repository, mock_user_service
):
    project_id = 15
    mock_user_service.get_user_by_id.return_value = project_model_stub

    await ProjectService.update_project(
        project_id=project_id, request=update_project_request_stub
    )

    mock_project_repository.update_project.assert_called_once_with(
        project_id=project_id, project_request=update_project_request_stub
    )
    mock_user_service.get_user_by_id.assert_called_once_with(user_id=1)


@pytest.mark.asyncio
async def test_when_create_new_project_then_verify_user_exists_is_called(
    mock_project_repository, mock_user_exists
):
    user_id = 10

    await ProjectService.verify_user_exists(user_id=user_id)

    mock_user_exists.get_user_by_id.assert_called_once_with(user_id=user_id)


@pytest.mark.asyncio
async def test_when_delete_project_by_id_then_repository_is_called(
    mock_project_repository,
):
    project_id = 15
    await ProjectService.delete_project_by_id(project_id)

    mock_project_repository.delete_one_project_by_id.assert_called_once_with(
        project_id=project_id
    )
