from typing import TypedDict
from src import UserModel


class PaginatedUsersTypedDict(TypedDict):
    users: list[UserModel]
    total: int
    limit: int
    offset: int
