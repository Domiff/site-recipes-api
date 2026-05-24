from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect

from src.auth.schemas import CredentialsSchema
from src.auth.service import register_user, login_user, logout_user
from src.core.config import settings
from src.core.database import SessionDep

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
    credentials: CredentialsSchema, session: SessionDep
) -> JSONResponse:
    response = JSONResponse(
        content={"detail": "User created successfully"},
        status_code=status.HTTP_201_CREATED,
    )
    session_id = await register_user(credentials, session)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=settings.session.SESSION_MAX_AGE,
        secure=True,
        samesite="lax",
    )
    return response


@router.post("/login")
async def login(
    credentials: CredentialsSchema, session: SessionDep
) -> JSONResponse:
    response = JSONResponse(
        content={"detail": "Logged in successfully"}, status_code=status.HTTP_200_OK
    )
    session_id = await login_user(credentials, session)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=settings.session.SESSION_MAX_AGE,
        secure=True,
        samesite="lax",
    )
    return response


@router.post("/logout")
async def logout(cookie_session_id: str) -> JSONResponse:
    response = JSONResponse(
        content={"detail": "Logged out successfully"},
        status_code=status.HTTP_204_NO_CONTENT,
    )
    await logout_user(cookie_session_id)
    response.delete_cookie("session_id")
    return response
