from src.domain.enums.http_response.internal_code import InternalCode


class BaseCustomException(Exception):
    def __init__(
        self,
        msg: str,
        status_code: int,
        internal_code: InternalCode,
        success: bool,
        *args,
        **kwargs
    ):
        self.msg = msg
        self.status_code = status_code
        self.internal_code = internal_code
        self.success = success
        super().__init__(msg, *args)


class DomainException(BaseCustomException):
    pass


class RepositoryException(BaseCustomException):
    pass


class ServiceException(BaseCustomException):
    pass


class InfrastructureException(BaseCustomException):
    pass
