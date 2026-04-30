from fastapi import HTTPException


class AppException(HTTPException):
    DETAIL = "Application Error"
    STATUS_CODE = 500

    def __init__(self, detail: str | None = None, status_code: int | None = None):
        super().__init__(
            status_code=status_code or self.STATUS_CODE,
            detail=detail or self.DETAIL,
        )


class AlreadyExists(AppException):
    DETAIL = "Already Exists"
    STATUS_CODE = 409


class IncorrectCredentials(AppException):
    DETAIL = "Incorrect Credentials"
    STATUS_CODE = 401


class DoesNotExist(AppException):
    DETAIL = "Not Found"
    STATUS_CODE = 404


class Unauthorized(AppException):
    DETAIL = "Unauthorized"
    STATUS_CODE = 401
