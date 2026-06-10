from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect

from src.auth.schemas import CredentialsSchema
from src.auth.service import AuthServiceDep
from src.core.config import settings

router = APIRouter(prefix="/auth")

CsrfProtectDep = Annotated[CsrfProtect, Depends()]


@router.get("/csrf-token")
async def get_csrf_token(csrf_protect: CsrfProtectDep) -> Response:
    response = Response()
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.post("/registration")
async def registration(
    service: AuthServiceDep, credentials: CredentialsSchema
) -> JSONResponse:
    response = JSONResponse(
        content={"detail": "User created successfully"},
        status_code=status.HTTP_201_CREATED,
    )
    session_id = await service.register(credentials)
    response.set_cookie(
        key=settings.session.SESSION_ID,
        value=session_id,
        httponly=True,
        max_age=settings.session.SESSION_MAX_AGE,
        secure=True,
        samesite="lax",
    )
    return response


@router.post("/login")
async def login(
    service: AuthServiceDep, credentials: CredentialsSchema
) -> JSONResponse:
    response = JSONResponse(
        content={"detail": "Logged in successfully"}, status_code=status.HTTP_200_OK
    )
    session_id = await service.login(credentials)
    response.set_cookie(
        key=settings.session.SESSION_ID,
        value=session_id,
        httponly=True,
        max_age=settings.session.SESSION_MAX_AGE,
        secure=True,
        samesite="lax",
    )
    return response


@router.post("/logout")
async def logout(service: AuthServiceDep, cookie_session_id: str) -> Response:
    response = Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
    await service.logout(cookie_session_id)
    response.delete_cookie(settings.session.SESSION_ID)
    return response
