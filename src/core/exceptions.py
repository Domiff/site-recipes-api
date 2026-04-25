from fastapi import HTTPException


class AppException(HTTPException):
    DETAIL = "Application Error"
    STATUS_CODE = 500

    def __init__(
        self, detail: str | None = None, status_code: int | None = None,
    ) -> None:
        if detail is None:
            self.detail = self.DETAIL
        if status_code is None:
            self.status_code = self.STATUS_CODE
        super().__init__(status_code=status_code, detail=detail)


class AlreadyExists(AppException):
    DETAIL = "Already Exists"
    STATUS_CODE = 409


class IncorrectCredentials(AppException):
    DETAIL = "Incorrect Credentials"
    STATUS_CODE = 401


class DoesNotExist(AppException):
    DETAIL = "Not Found"
    STATUS_CODE = 404
