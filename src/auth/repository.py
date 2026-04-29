from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.auth.schemas import CredentialsSchema, UserSchema
from src.auth.utils import hash_password, verify_password, generate_session_id
from src.core.exceptions import AlreadyExists, IncorrectCredentials, DoesNotExist
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
        query = select(User).where(User.email == email, User.is_active)
        result = await self.session.execute(query)
        user = result.scalar_one()
        if not user:
            raise DoesNotExist("User not found")
        return user

    async def get_user_by_username(self, username: str) -> User:
        query = select(User).where(User.username == username, User.is_active)
        result = await self.session.execute(query)
        user = result.scalar_one()
        if not user:
            raise DoesNotExist("User not found")
        return user

    async def authenticate(self, credentials: CredentialsSchema = None, user_model: User = None) -> str:
        if user_model:
            return generate_session_id(32)
        if not credentials:
            raise IncorrectCredentials("Incorrect credentials")
        if credentials.email:
            user = await self.get_user_by_email(credentials.email)
        elif credentials.username:
            user = await self.get_user_by_username(credentials.username)
        else:
            raise IncorrectCredentials("Incorrect credentials")
        user = UserSchema.model_validate(user, from_attributes=True)
        if not verify_password(credentials.password, user.password):
            logger.error("Incorrect password")
            raise IncorrectCredentials("Incorrect credentials")
        return generate_session_id(32)
