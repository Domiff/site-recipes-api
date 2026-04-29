from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError

from src.core.logging_app import get_logger

logger = get_logger(__name__)


async def _csrf_protect_exception_handler(
    request: Request, exc: CsrfProtectError
) -> JSONResponse:
    logger.error(exc.message)
    return JSONResponse(
        status_code=exc.status_code, content={"detail": "Error with CSRF protection"}
    )


def setup_errors(app: FastAPI) -> None:
    app.add_exception_handler(CsrfProtectError, _csrf_protect_exception_handler)
