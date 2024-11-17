from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Response

from src.domain.enums.http_response.internal_code import InternalCode
from src.domain.models.http_response.model import ResponseModel


class ClientsRouter:
    __router = APIRouter(prefix="/api/v1", tags=["Partners Loader"])

    @staticmethod
    def get_clients_router():
        return ClientsRouter.__router

    @staticmethod
    @__router.get(path="/clients", response_model=List["bananinha"])
    async def list_all() -> Response:
        result = await ClientsService.get_all_partners()
        response = ResponseModel(
            result=result, internal_code=InternalCode.SUCCESS, success=True
        ).build_http_response(
            status_code=HTTPStatus.OK,
        )
        return response
