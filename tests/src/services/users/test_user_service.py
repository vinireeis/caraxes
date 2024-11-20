from unittest.mock import patch

import pytest

from src import UserModel
from src.services.users.service import UserService
from tests.src.services.stubs import (
    user_model_stub,
    new_user_request_stub,
    updated_user_model_stub,
    update_user_request_stub,
    user_paginated_result_stub,
)


@pytest.mark.asyncio
@patch(
    "src.services.users.service.UserService._user_repository.insert_one_user",
    return_value=user_model_stub,
)
async def test_when_create_new_user_then_return_user_model(mock_user_repository):

    user_model = await UserService.create_new_user(request=new_user_request_stub)

    assert isinstance(user_model, UserModel)
    assert user_model.name == "John Doe"
    assert user_model.email == "test@example.com"
    assert user_model.role == "dev"
    assert user_model.id == 10


@pytest.mark.asyncio
@patch(
    "src.services.users.service.UserService._user_repository.get_one_user_by_id",
    return_value=user_model_stub,
)
async def test_when_get_user_by_id_then_return_user_model(mock_get_user_by_id):
    user_id = 10
    user_model = await UserService.get_user_by_id(user_id=user_id)

    mock_get_user_by_id.assert_called_once_with(user_id=user_id)
    assert isinstance(user_model, UserModel)
    assert user_model.id == 10
    assert user_model.name == "John Doe"
    assert user_model.email == "test@example.com"
    assert user_model.role == "dev"


@pytest.mark.asyncio
@patch(
    "src.services.users.service.UserService._user_repository.get_users_paginated",
    return_value=user_paginated_result_stub,
)
async def test_when_get_users_paginated_then_return_paginated_users_typed_dict(
    mock_get_users_paginated,
):
    limit = 10
    offset = 0
    paginated_result = await UserService.get_users_paginated(limit=limit, offset=offset)

    mock_get_users_paginated.assert_called_once_with(limit=limit, offset=offset)
    assert isinstance(paginated_result, dict)
    assert len(paginated_result["users"]) == 1
    assert paginated_result["total"] == 1
    assert paginated_result["limit"] == 10
    assert paginated_result["offset"] == 0
    assert paginated_result["users"][0].id == 10


@pytest.mark.asyncio
@patch("src.services.users.service.UserService._user_repository.delete_one_user_by_id")
async def test_when_delete_user_by_id_then_repository_is_called(mock_delete_user):
    user_id = 10
    await UserService.delete_user_by_id(user_id=user_id)

    mock_delete_user.assert_called_once_with(user_id=user_id)


@pytest.mark.asyncio
@patch(
    "src.services.users.service.UserService._user_repository.insert_one_user",
    return_value=user_model_stub,
)
async def test_when_create_new_user_then_return_user_model(mock_user_repository):
    user_model = await UserService.create_new_user(request=new_user_request_stub)

    assert isinstance(user_model, UserModel)
    assert user_model.name == "John Doe"
    assert user_model.email == "test@example.com"
    assert user_model.role == "dev"
    assert user_model.id == 10


@pytest.mark.asyncio
@patch(
    "src.services.users.service.UserService._user_repository.update_user",
    return_value=updated_user_model_stub,
)
async def test_when_update_user_by_id_then_return_user_model_updated(
    mock_user_repository,
):
    success_result = await UserService.update_user_by_id(
        user_id=10, request=update_user_request_stub
    )

    assert success_result is None


@pytest.mark.asyncio
@patch("src.services.users.service.UserService._user_repository.update_user")
async def test_when_update_user_then_repository_is_called_with_correct_arguments(
    mock_update_user,
):
    await UserService.update_user_by_id(user_id=10, request=update_user_request_stub)

    mock_update_user.assert_called_once()
    mock_update_user.assert_called_once_with(
        user_id=10, update_user_request=update_user_request_stub
    )


@pytest.mark.asyncio
@patch("src.services.users.service.UserService._user_repository.delete_one_user_by_id")
async def test_when_delete_user_by_id_then_repository_is_called(mock_delete_user):
    user_id = 10
    await UserService.delete_user_by_id(user_id=user_id)

    mock_delete_user.assert_called_once_with(user_id=user_id)
