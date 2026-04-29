from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repository import AuthUser, AuthSession
from src.auth.schemas import CredentialsSchema
from src.core.logging_app import get_logger
from src.core.redis import RedisClient


logger = get_logger(__name__)

async def register_user(credentials: CredentialsSchema, session: AsyncSession) -> str:
    redis = RedisClient()
    auth_user = AuthUser(session=session)
    auth_session = AuthSession(session=session)
    user = await auth_user.create_user(credentials)
    session_id = await auth_user.authenticate(user_model=user)
    await auth_session.create_session(session_id, user.username)
    await redis.set(session_id, user.username)
    return session_id


async def login_user(credentials: CredentialsSchema, session: AsyncSession, cookie_session_id) -> str:
    redis = RedisClient()
    auth_user = AuthUser(session=session)
    auth_session = AuthSession(session=session)
    session_id = await auth_user.authenticate(credentials=credentials)
    await auth_session.update_session(session_id)
    await redis.expire(cookie_session_id)
    return session_id

# TODO: add refresh, check for cache

async def logout_user(cookie_session_id: str, session: AsyncSession) -> bool:
    redis = RedisClient()
    auth_session = AuthSession(session=session)
    await auth_session.delete_session(cookie_session_id)
    await redis.delete(cookie_session_id)
    return True
