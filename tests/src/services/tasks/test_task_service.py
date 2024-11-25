from unittest.mock import AsyncMock, call, patch

import pytest

from src import UserModel, TaskModel
from src.adapters.data_types.requests.tasks_request import UpdateTaskStatusRequest
from src.domain.enums.projects.enum import ProjectStatusEnum
from src.domain.enums.tasks.enum import TaskStatusEnum
from src.domain.exceptions.repository.exception import UserNotFoundError
from src.domain.exceptions.service.exception import (
    InvalidAssignedUserError,
    InvalidProjectStatusForTaskCreationError,
)
from src.services.tasks.service import TaskService
from tests.src.services.stubs import (
    new_task_request_stub,
    paginated_tasks_stub,
    project_model_stub,
    project_model_with_status_stub,
    task_model_stub,
    update_task_request_stub,
    user_model_stub,
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
        await TaskService.validate_project_status_is_planning_or_active(
            project_id=project_id
        )


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
        await TaskService.validate_project_status_is_planning_or_active(
            project_id=project_id
        )


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
        await TaskService.validate_project_status_is_planning_or_active(
            project_id=project_id
        )


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


@pytest.mark.asyncio
@patch(
    "src.services.tasks.service.TaskService._user_service.get_user_by_id",
    new_callable=AsyncMock,
)
async def test_when_validate_users_assigned_ids_already_exists_and_all_users_exist_then_return_list_of_user_models(
    mock_get_user_by_id,
):
    mock_get_user_by_id.side_effect = [
        user_model_stub for _ in new_task_request_stub.assigned_users
    ]

    result = await TaskService.validate_users_assigned_ids_already_exists(
        request=new_task_request_stub
    )

    mock_get_user_by_id.assert_has_calls(
        [call(user_id=user_id) for user_id in new_task_request_stub.assigned_users]
    )
    assert isinstance(result, list)
    assert all(isinstance(user, UserModel) for user in result)
    assert len(result) == len(new_task_request_stub.assigned_users)


@pytest.mark.asyncio
@patch(
    "src.services.tasks.service.TaskService._user_service.get_user_by_id",
    new_callable=AsyncMock,
)
async def test_when_assigned_user_not_found_then_raise_invalid_assigned_user_error(
    mock_get_user_by_id,
):
    mock_get_user_by_id.side_effect = [user_model_stub, UserNotFoundError(user_id=15)]

    with pytest.raises(InvalidAssignedUserError):
        await TaskService.validate_users_assigned_ids_already_exists(
            request=new_task_request_stub
        )

    mock_get_user_by_id.assert_has_calls(
        [call(user_id=user_id) for user_id in new_task_request_stub.assigned_users]
    )


@pytest.mark.asyncio
@patch(
    "src.services.tasks.service.TaskService.validate_project_status_is_planning_or_active",
    new_callable=AsyncMock,
)
@patch(
    "src.services.tasks.service.TaskService._task_repository.update_task",
    new_callable=AsyncMock,
)
async def test_when_update_task_then_repository_is_called_with_correct_arguments(
    mock_update_task, mock_validate_project_status
):
    project_id = 1
    task_id = 10

    await TaskService.update_task(
        project_id=project_id, task_id=task_id, request=update_task_request_stub
    )

    mock_validate_project_status.assert_called_once_with(project_id=project_id)
    mock_update_task.assert_called_once_with(
        project_id=project_id, task_id=task_id, task_request=update_task_request_stub
    )


@pytest.mark.asyncio
@patch(
    "src.services.tasks.service.TaskService.validate_project_status_is_planning_or_active",
    new_callable=AsyncMock,
)
@patch(
    "src.services.tasks.service.TaskService._task_repository.insert_one_task",
    new_callable=AsyncMock,
)
@patch(
    "src.services.tasks.service.TaskService.validate_users_assigned_ids_already_exists",
    new_callable=AsyncMock,
)
async def test_when_create_new_task_then_task_is_created_with_correct_arguments(
    mock_validate_users, mock_insert_task, mock_validate_project_status
):
    project_id = 1
    mock_validate_users.return_value = []
    mock_insert_task.return_value = task_model_stub

    new_task = await TaskService.create_new_task(
        project_id=project_id, request=new_task_request_stub
    )

    mock_validate_project_status.assert_called_once_with(project_id=project_id)
    mock_validate_users.assert_called_once_with(request=new_task_request_stub)
    mock_insert_task.assert_called_once_with(
        project_id=project_id, task_request=new_task_request_stub, users_model=[]
    )

    assert isinstance(new_task, TaskModel)
    assert new_task == task_model_stub


@pytest.mark.asyncio
@patch(
    "src.services.tasks.service.TaskService.validate_project_status_is_planning_or_active",
    new_callable=AsyncMock,
)
@patch(
    "src.services.tasks.service.TaskService._task_repository.insert_one_task",
    new_callable=AsyncMock,
)
@patch(
    "src.services.tasks.service.TaskService.validate_users_assigned_ids_already_exists",
    new_callable=AsyncMock,
)
async def test_when_create_new_task_with_assigned_users_then_users_are_validated(
    mock_validate_users, mock_insert_task, mock_validate_project_status
):
    project_id = 1
    assigned_users = [1, 2]
    new_task_request_stub.assigned_users = assigned_users
    mock_validate_users.return_value = [user_model_stub]
    mock_insert_task.return_value = task_model_stub

    new_task = await TaskService.create_new_task(
        project_id=project_id, request=new_task_request_stub
    )

    mock_validate_project_status.assert_called_once_with(project_id=project_id)
    mock_validate_users.assert_called_once_with(request=new_task_request_stub)
    mock_insert_task.assert_called_once_with(
        project_id=project_id,
        task_request=new_task_request_stub,
        users_model=[user_model_stub],
    )

    assert isinstance(new_task, TaskModel)
    assert new_task == task_model_stub
