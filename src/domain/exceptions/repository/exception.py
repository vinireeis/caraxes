from http import HTTPStatus

from src.domain.enums.http_response.internal_code import InternalCode
from src.domain.exceptions.base.exception import RepositoryException


class Base64DecodeError(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error to decode Base64"
        self.status_code = HTTPStatus.BAD_REQUEST
        self.internal_code = InternalCode.DATA_DECODER_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
