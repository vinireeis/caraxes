from typing import Annotated

from decouple import config
from fastapi import APIRouter, Query

from src.adapters.data_types.requests.users_request import (
    NewUserRequest,
    UpdateUserRequest,
)
from src.adapters.data_types.responses.users_response import (
    UsersPaginatedResponse,
    GetOneUserResponse,
    NewUserResponse,
    DeleteUserResponse,
    UpdateUserResponse,
)
from src.services.users.service import UserService


class UsersRouter:
    __router = APIRouter(prefix=config("ROOT_PATH"), tags=["Users"])

    @staticmethod
    def get_users_router():
        return UsersRouter.__router

    @staticmethod
    @__router.get(path="/users", response_model=UsersPaginatedResponse)
    async def get_users_paginated(
        limit: Annotated[int, Query(default=10, ge=1)],
        offset: Annotated[int, Query(default=0, ge=0)],
    ) -> UsersPaginatedResponse:
        response = await UserService.get_users_paginated(limit=limit, offset=offset)

        return response

    @staticmethod
    @__router.get(path="/users/{user_id}", response_model=GetOneUserResponse)
    async def get_one_user(user_id: int) -> GetOneUserResponse:
        response = await UserService.get_user_by_id(user_id=user_id)

        return response

    @staticmethod
    @__router.post(path="/users", response_model=NewUserResponse)
    async def create_new_user(request: NewUserRequest) -> NewUserResponse:
        response = await UserService.create_new_user(
            request=request,
        )

        return response

    @staticmethod
    @__router.put(path="/users/{user_id}", response_model=UpdateUserResponse)
    async def update_user(
        user_id: int, request: UpdateUserRequest
    ) -> UpdateUserResponse:
        response = await UserService.update_user_by_id(user_id=user_id, request=request)

        return response

    @staticmethod
    @__router.delete(path="/users/{user_id}", response_model=DeleteUserResponse)
    async def delete_user(user_id: int) -> DeleteUserResponse:
        response = await UserService.delete_user_by_id(user_id=user_id)

        return response
