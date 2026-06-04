from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User, Session
from src.auth.schemas import CredentialsSchema
from src.auth.utils import hash_password, expire_at
from src.core.config import settings
from src.core.exceptions import AlreadyExists, DoesNotExist
from src.core.logging_app import get_logger


logger = get_logger(__name__)


class BaseAuth:
    def __init__(self, session: AsyncSession):
        self.session = session


class AuthUser(BaseAuth):
    async def create_user(self, credentials: CredentialsSchema) -> User:
        hashed_password = hash_password(credentials.password)
        try:
            user = User(
                email=credentials.email,
                password=hashed_password,
                username=credentials.username,
            )
            self.session.add(user)
            await self.session.commit()
            logger.info("User registered")
            return user
        except IntegrityError:
            logger.error("User already exists")
            await self.session.rollback()
            raise AlreadyExists("User already exists")

    async def get_user_by_email(self, email: str) -> User:
        try:
            query = select(User).where(User.email == email, User.is_active)
            result = await self.session.execute(query)
            user = result.scalar_one()
            return user
        except NoResultFound:
            raise DoesNotExist("User not found")


class AuthSession(BaseAuth):
    async def create_session(self, session_key, session_data, user) -> Session:
        session = Session(
            session_key=session_key,
            session_data=session_data,
            expire_date=expire_at(),
            user=user,
        )
        self.session.add(session)
        await self.session.commit()
        logger.info("Session created")
        return session

    async def delete_session(self, session_key) -> bool:
        await self.session.delete(session_key)
        await self.session.commit()
        logger.info("Session deleted")
        return True

    async def update_session(self, session_key) -> bool:
        session = select(Session).where(session_key=session_key)
        session.expire_date = datetime.now() + timedelta(
            seconds=settings.session.SESSION_MAX_AGE
        )
        self.session.add(session)
        await self.session.commit()
        logger.info("Session updated")
        return True
