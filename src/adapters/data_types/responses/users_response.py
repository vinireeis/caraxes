from pydantic import BaseModel, Field

from src.adapters.data_types.responses.base.base_response import BaseResponse


class UserPayload(BaseModel):
    id: int
    name: str
    email: str
    role: str | None


class UsersPaginatedPayload(BaseModel):
    users: list[UserPayload] = Field(default_factory=list)
    total: int
    limit: int
    offset: int


class UserIdPayload(BaseModel):
    id: int


class UsersPaginatedResponse(BaseResponse):
    payload: UsersPaginatedPayload


class GetOneUserResponse(BaseResponse):
    payload: UserPayload


class NewUserResponse(BaseResponse):
    payload: UserIdPayload


class UpdateUserResponse(BaseResponse):
    pass


class DeleteUserResponse(BaseResponse):
    pass
