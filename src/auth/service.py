from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.repository import get_session_repo, get_user_repo
from src.auth.schemas import CredentialsSchema, UserSchema
from src.auth.utils import generate_session_id, verify_password
from src.core.database import SessionDep
from src.core.exceptions import IncorrectCredentials
from src.core.logging_app import get_logger
from src.core.redis import RedisClient

logger = get_logger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = get_user_repo(self.session)
        self.session_repo = get_session_repo(self.session)
        self.redis = RedisClient()

    async def register(self, credentials: CredentialsSchema) -> str:
        user = await self.user_repo.create(credentials)
        session_id = await self.authenticate(user_model=user)
        await self.session_repo.create(session_id, user.username, user)
        await self.redis.set(session_id, user.username)
        logger.info("User registered", session_id=session_id)
        return session_id

    async def login(self, credentials: CredentialsSchema) -> str:
        session_id = await self.authenticate(credentials=credentials)
        await self.redis.set(session_id, credentials.username)
        logger.info("User logged in", session_id=session_id)
        return session_id

    async def logout(self, cookie_session_id: str) -> bool:
        await self.redis.delete(cookie_session_id)
        await self.session_repo.delete(cookie_session_id)
        logger.info("User logged out", session_id=cookie_session_id)
        return True

    async def authenticate(
        self, credentials: CredentialsSchema = None, user_model: User = None
    ) -> str:
        if user_model:
            return generate_session_id(32)
        if credentials:
            user = await self.user_repo.get_user_by_email(credentials.email)
        else:
            raise IncorrectCredentials("Incorrect credentials")
        user = UserSchema.model_validate(user, from_attributes=True)
        if not verify_password(credentials.password, user.password):
            logger.error("Incorrect password")
            raise IncorrectCredentials("Incorrect credentials")
        return generate_session_id(32)


def get_auth_service(session: SessionDep) -> AuthService:
    return AuthService(session)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
