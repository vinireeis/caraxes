from unittest.mock import patch

import pytest

from src.domain.enums.projects.enum import ProjectStatusEnum
from src.domain.exceptions.service.exception import (
    InvalidProjectStatusForTaskCreationError,
)
from src.domain.enums.tasks.enum import TaskStatusEnum
from src.adapters.data_types.requests.tasks_request import UpdateTaskStatusRequest
from src.services.tasks.service import TaskService
from tests.src.services.stubs import (
    project_model_with_status_stub,
    user_model_stub,
    new_task_request_stub,
    task_model_stub,
    paginated_tasks_stub,
    update_task_request_stub,
    project_model_stub,
)


@pytest.mark.asyncio
@patch(
    "src.services.tasks.service.TaskService._task_repository.get_one_task_by_id",
    return_value=task_model_stub,
)
async def test_when_get_task_by_id_then_return_task(mock_get_task_by_id):
    task = await TaskService.get_task_by_id(project_id=15, task_id=1)

    mock_get_task_by_id.assert_called_once_with(project_id=15, task_id=1)
    assert task.id == 1
    assert task.name == "Task 1"


@pytest.mark.asyncio
@patch(
    "src.services.tasks.service.TaskService._task_repository.get_tasks_paginated",
    return_value=paginated_tasks_stub,
)
async def test_when_get_tasks_paginated_then_return_tasks(mock_get_tasks_paginated):
    tasks = await TaskService.get_tasks_paginated(limit=10, offset=0)

    mock_get_tasks_paginated.assert_called_once_with(
        limit=10, offset=0, project_id=None, user_id=None
    )
    assert len(tasks["tasks"]) == 1
    assert tasks["tasks"][0].name == "Task 1"


@pytest.mark.asyncio
@patch("src.services.tasks.service.TaskService._task_repository.delete_one_task_by_id")
async def test_when_delete_task_then_repository_is_called(mock_delete_task):
    await TaskService.delete_task(project_id=15, task_id=1)

    mock_delete_task.assert_called_once_with(project_id=15, task_id=1)


@pytest.mark.asyncio
@patch("src.services.tasks.service.TaskService._task_repository.update_task_status")
@patch(
    "src.services.tasks.service.TaskService._project_service.get_project_by_id",
    return_value=project_model_stub,
)
async def test_when_update_task_status_then_repository_is_called_with_correct_arguments(
    mock_get_project, mock_update_task_status
):
    project_id = 15
    task_id = 1
    update_task_status_request_stub = UpdateTaskStatusRequest(
        status=TaskStatusEnum.DONE
    )

    await TaskService.update_task_status(
        project_id=project_id, task_id=task_id, request=update_task_status_request_stub
    )

    mock_update_task_status.assert_called_once_with(
        project_id=project_id,
        task_id=task_id,
        status=TaskStatusEnum.DONE,
    )


@pytest.mark.asyncio
@patch(
    "src.services.projects.service.ProjectService.get_project_by_id",
    return_value=project_model_with_status_stub,
)
async def test_when_validate_project_status_is_canceled_then_raises(
    mock_get_project_by_id,
):
    project_id = 1

    with pytest.raises(InvalidProjectStatusForTaskCreationError):
        await TaskService.validate_project_status_is_planning_or_active(project_id)


@pytest.mark.asyncio
@patch(
    "src.services.projects.service.ProjectService.get_project_by_id",
    return_value=project_model_with_status_stub,
)
async def test_when_validate_project_status_is_paused_then_raises(
    mock_get_project_by_id,
):
    project_model_with_status_stub.status = ProjectStatusEnum.PAUSED
    project_id = 1

    with pytest.raises(InvalidProjectStatusForTaskCreationError):
        await TaskService.validate_project_status_is_planning_or_active(project_id)


@pytest.mark.asyncio
@patch(
    "src.services.projects.service.ProjectService.get_project_by_id",
    return_value=project_model_with_status_stub,
)
async def test_when_validate_project_status_is_completed_then_raises(
    mock_get_project_by_id,
):
    project_model_with_status_stub.status = ProjectStatusEnum.PAUSED
    project_id = 1

    with pytest.raises(InvalidProjectStatusForTaskCreationError):
        await TaskService.validate_project_status_is_planning_or_active(project_id)


@pytest.mark.asyncio
@patch(
    "src.services.projects.service.ProjectService.get_project_by_id",
    return_value=project_model_stub,
)
async def test_when_validate_project_status_is_planning_then_success(
    mock_get_project_by_id,
):
    project_model_stub.status = ProjectStatusEnum.PLANNING
    project_id = 1

    await TaskService.validate_project_status_is_planning_or_active(
        project_id=project_id
    )

    mock_get_project_by_id.assert_called_once_with(project_id=project_id)


@pytest.mark.asyncio
@patch(
    "src.services.projects.service.ProjectService.get_project_by_id",
    return_value=project_model_stub,
)
async def test_when_validate_project_status_is_active_then_success(
    mock_get_project_by_id,
):
    project_model_stub.status = ProjectStatusEnum.ACTIVE
    project_id = 1

    await TaskService.validate_project_status_is_planning_or_active(
        project_id=project_id
    )

    mock_get_project_by_id.assert_called_once_with(project_id=project_id)
