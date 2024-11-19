from http import HTTPStatus

from decouple import config
from fastapi import APIRouter, Query

from src.adapters.controllers.caraxes_controller import CaraxesController
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


class UsersRouter:
    __router = APIRouter(prefix=config("ROOT_PATH"), tags=["Users"])

    @staticmethod
    def get_users_router():
        return UsersRouter.__router

    @staticmethod
    @__router.get(path="/users", response_model=UsersPaginatedResponse, response_model_exclude_none=True)
    async def get_users_paginated(
        limit: int = Query(default=10, ge=1),
        offset: int = Query(default=0, ge=0),
    ) -> UsersPaginatedResponse:
        response = await CaraxesController.get_users_paginated(
            limit=limit, offset=offset
        )

        return response

    @staticmethod
    @__router.get(path="/users/{user_id}", response_model=GetOneUserResponse, response_model_exclude_none=True)
    async def get_one_user(user_id: int) -> GetOneUserResponse:
        response = await CaraxesController.get_user_by_id(user_id=user_id)

        return response

    @staticmethod
    @__router.post(path="/users", response_model=NewUserResponse, response_model_exclude_none=True)
    async def create_new_user(request: NewUserRequest) -> NewUserResponse:
        response = await CaraxesController.create_new_user(
            request=request,
        )

        return response

    @staticmethod
    @__router.put(path="/users/{user_id}", response_model=UpdateUserResponse, response_model_exclude_none=True)
    async def update_user(
        user_id: int, request: UpdateUserRequest
    ) -> UpdateUserResponse:
        response = await CaraxesController.update_user_by_id(
            user_id=user_id, request=request
        )

        return response

    @staticmethod
    @__router.delete(path="/users/{user_id}", response_model=DeleteUserResponse, response_model_exclude_none=True)
    async def delete_user(user_id: int) -> DeleteUserResponse:
        response = await CaraxesController.delete_user_by_id(user_id=user_id)

        return response
