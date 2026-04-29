from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository import Auth
from src.auth.schemas import CredentialsSchema
from src.core.logging_app import get_logger
from src.core.redis import RedisClient


logger = get_logger(__name__)

async def register_user(credentials: CredentialsSchema, session: AsyncSession) -> str:
    async with Auth(session=session) as auth, RedisClient() as redis:
        user = await auth.create_user(credentials)
        session_id = await auth.authenticate(user_model=user)
        await redis.set(session_id, user.username)
    return session_id


async def login_user(credentials: CredentialsSchema, session: AsyncSession, cookie_session_id) -> str:
    async with Auth(session=session) as auth, RedisClient() as redis:
        session_id = await auth.authenticate(credentials=credentials)
        email_or_username = credentials.email if credentials.email else credentials.username
        await redis.delete(cookie_session_id)
        await redis.set(session_id, email_or_username)
    return session_id


async def logout_user(cookie_session_id: str) -> bool:
    async with RedisClient() as redis:
        await redis.delete(cookie_session_id)
        return True
