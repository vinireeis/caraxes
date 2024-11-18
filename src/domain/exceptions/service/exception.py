from http import HTTPStatus

from src.domain.enums.http_response.enum import InternalCodeEnum
from src.domain.exceptions.base.exception import ServiceException


class InvalidProjectStatusForTaskCreationError(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Project status should be in active or planing"
        self.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        self.internal_code = InternalCodeEnum.INVALID_PROJECT_STATUS_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class InvalidAssignedUserError(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "One or more assigned users do not exist"
        self.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        self.internal_code = InternalCodeEnum.INVALID_USER_ID_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
