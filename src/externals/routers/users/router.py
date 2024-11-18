from http import HTTPStatus

from fastapi import APIRouter, Response

from src.domain.enums.http_response.internal_code import InternalCode
from src.domain.models.http_response.model import ResponseModel


class UsersRouter:
    __router = APIRouter(prefix="/api/v1", tags=["Partners Loader"])

    @staticmethod
    def get_users_router():
        return UsersRouter.__router

    @staticmethod
    @__router.get(path="/clients", response_model=None)
    async def list_all() -> Response:
        result = "await UsersService.get_all_partners()"
        response = ResponseModel(
            result=result, internal_code=InternalCode.SUCCESS, success=True
        ).build_http_response(
            status_code=HTTPStatus.OK,
        )
        return response
