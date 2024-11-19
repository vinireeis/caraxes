from http import HTTPStatus
from time import time

from loguru import logger
from fastapi import Request, Response, FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.adapters.data_types.responses.base.error_response import ErrorResponse
from src.domain.enums.http_response.enum import InternalCodeEnum
from src.domain.exceptions.base.exception import (
    InfrastructureException,
    RepositoryException,
)
from src.domain.exceptions.domain.exception import DomainException
from src.domain.exceptions.service.exception import ServiceException


class Middleware:

    @staticmethod
    def register_middleware(app: FastAPI):

        @app.middleware("http")
        async def process_request(request: Request, call_next: callable) -> Response:
            start_time = time()
            response = await Middleware._response_handler(
                request=request, call_next=call_next
            )
            process_time = time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response

    @staticmethod
    async def _response_handler(request: Request, call_next: callable):
        response = None

        try:
            response = await call_next(request)

        except (
            DomainException,
            ServiceException,
            RepositoryException,
            InfrastructureException,
        ) as ex:
            logger.info(ex.msg)
            error_response = ErrorResponse(
                success=False,
                message=ex.msg,
                internal_code=ex.internal_code,
            )
            response = JSONResponse(
                status_code=ex.status_code, content=error_response.model_dump()
            )

        except ValidationError as ex:
            logger.info(ex.msg)
            error_response = ErrorResponse(
                success=False,
                internal_code=InternalCodeEnum.DATA_VALIDATION_ERROR,
                message=str(ex),
            )
            response = JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=error_response.model_dump(),
            )

        except Exception as ex:
            logger.info(ex)
            error_response = ErrorResponse(
                success=False,
                internal_code=InternalCodeEnum.INTERNAL_SERVER_ERROR,
            )
            response = JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content=error_response.model_dump(),
            )

        finally:
            return response
