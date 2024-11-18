from http import HTTPStatus
from pydantic import BaseModel

from src.domain.enums.http_response.enum import InternalCodeEnum


class BaseResponse(BaseModel):
    success: bool = False
    internal_code: InternalCodeEnum
    message: str = None
    status_code: HTTPStatus = None
