from datetime import datetime, timedelta

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import Session, User
from src.auth.schemas import CredentialsSchema
from src.auth.utils import expire_at, hash_password
from src.core.config import settings
from src.core.database import BaseRepository
from src.core.exceptions import AlreadyExists, DoesNotExist
from src.core.logging_app import get_logger

logger = get_logger(__name__)


class UserRepository(BaseRepository):
    async def create(self, credentials: CredentialsSchema) -> User:
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
        except IntegrityError as err:
            logger.error("User already exists")
            await self.session.rollback()
            raise AlreadyExists("User already exists") from err

    async def get_user_by_email(self, email: str) -> User:
        try:
            query = select(User).where(User.email == email, User.is_active)
            result = await self.session.execute(query)
            user = result.scalar_one()
            return user
        except NoResultFound as err:
            raise DoesNotExist("User not found") from err


class SessionRepository(BaseRepository):
    async def create(self, session_key, session_data, user) -> Session:
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

    async def delete(self, session_key) -> bool:
        stmt = delete(Session).where(session_key == session_key)
        await self.session.execute(stmt)
        await self.session.commit()
        logger.info("Session deleted")
        return True

    async def update(self, session_key) -> bool:
        session = (
            update(Session)
            .where(session_key == session_key)
            .values(
                expire_date=datetime.now()
                + timedelta(seconds=settings.session.SESSION_MAX_AGE)
            )
        )
        await self.session.execute(session)
        await self.session.commit()
        logger.info("Session updated")
        return True


def get_user_repo(session: AsyncSession) -> UserRepository:
    return UserRepository(session)


def get_session_repo(session: AsyncSession) -> SessionRepository:
    return SessionRepository(session)
