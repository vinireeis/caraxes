from http import HTTPStatus
from time import time

import loglifos
from fastapi import Request, Response
from pydantic import ValidationError

from src.adapters.data_types.responses.base.error_response import ErrorResponse
from src.domain.enums.http_response.enum import InternalCodeEnum
from src.domain.exceptions.base.exception import (
    InfrastructureException,
    RepositoryException,
)
from src.domain.exceptions.domain.exception import DomainException
from src.domain.exceptions.service.exception import ServiceException
from src.externals.infrastructures.api.infrastructure import ApiInfrastructure


class Middleware:
    __app = ApiInfrastructure.get_app()

    @classmethod
    @__app.middleware("http")
    async def process_request(cls, request: Request, call_next: callable) -> Response:
        start_time = time()
        response = await cls.__response_handler(request=request, call_next=call_next)
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    @staticmethod
    async def __response_handler(request: Request, call_next: callable):
        response = None

        try:
            response = await call_next(request)

        except (
            DomainException,
            ServiceException,
            RepositoryException,
            InfrastructureException,
        ) as ex:
            loglifos.info(msg=ex.msg)
            response = ErrorResponse(
                success=False,
                message=ex.msg,
                internal_code=ex.internal_code,
                status_code=ex.status_code,
            )

        except ValidationError as ex:
            loglifos.error(exception=ex, msg=str(ex))
            response = ErrorResponse(
                success=False,
                internal_code=InternalCodeEnum.DATA_VALIDATION_ERROR,
                status_code=HTTPStatus.BAD_REQUEST,
            )

        except Exception as ex:
            loglifos.error(exception=ex, msg=str(ex))
            response = ErrorResponse(
                success=False,
                internal_code=InternalCodeEnum.INTERNAL_SERVER_ERROR,
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        finally:
            return response
