from http import HTTPStatus

from src.domain.enums.http_response.enum import InternalCodeEnum
from src.domain.exceptions.base.exception import RepositoryException


class UserNotFoundError(RepositoryException):
    def __init__(self, user_id, *args, **kwargs):
        self.msg = f"User with ID {user_id} not found."
        self.status_code = HTTPStatus.NOT_FOUND
        self.internal_code = InternalCodeEnum.DATA_NOT_FOUND
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs,
        )


class EmailAlreadyExists(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = f"User with this email already exists."
        self.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        self.internal_code = InternalCodeEnum.DATA_ALREADY_EXISTS
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs,
        )


class ProjectNotFoundError(RepositoryException):
    def __init__(self, project_id, *args, **kwargs):
        self.msg = f"Project with ID {project_id} not found."
        self.status_code = HTTPStatus.NOT_FOUND
        self.internal_code = InternalCodeEnum.DATA_NOT_FOUND
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs,
        )


class TaskNotFoundError(RepositoryException):
    def __init__(self, task_id, *args, **kwargs):
        self.msg = f"Task with ID {task_id} not found."
        self.status_code = HTTPStatus.NOT_FOUND
        self.internal_code = InternalCodeEnum.DATA_NOT_FOUND
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs,
        )
