from src import UserModel
from src.adapters.data_types.requests.users_request import (
    NewUserRequest,
    UpdateUserRequest,
)
from src.adapters.data_types.typed_dicts.users_typed_dict import PaginatedUsersTypedDict
from src.adapters.repositories.users.repository import UserRepository


class UserService:

    _user_repository: UserRepository = UserRepository()

    @classmethod
    async def create_new_user(cls, request: NewUserRequest) -> UserModel:
        new_user_model = await cls._user_repository.insert_one_user(
            user_request=request
        )

        return new_user_model

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> UserModel:
        user_model = await cls._user_repository.get_one_user_by_id(user_id=user_id)

        return user_model

    @classmethod
    async def get_users_paginated(
        cls, limit: int, offset: int
    ) -> PaginatedUsersTypedDict:

        users_paginated_result = await cls._user_repository.get_users_paginated(
            limit=limit, offset=offset
        )

        return users_paginated_result

    @classmethod
    async def update_user_by_id(cls, user_id: int, request: UpdateUserRequest):
        await cls._user_repository.update_user(
            user_id=user_id, update_user_request=request
        )

    @classmethod
    async def delete_user_by_id(cls, user_id: int):
        await cls._user_repository.delete_one_user_by_id(user_id=user_id)
