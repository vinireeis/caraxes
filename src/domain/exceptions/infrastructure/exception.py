from http import HTTPStatus

from src.domain.enums.http_response.enum import InternalCodeEnum
from src.domain.exceptions.base.exception import InfrastructureException


class SqlAlchemyInfrastructureException(InfrastructureException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error trying to get session"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCodeEnum.INFRASTRUCTURE_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class UnexpectedInfrastructureException(InfrastructureException):
    def __init__(self, *args, **kwargs):
        self.msg = "Unexpected infrastructure exception"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCodeEnum.INFRASTRUCTURE_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
