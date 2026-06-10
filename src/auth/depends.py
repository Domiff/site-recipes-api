from fastapi import Depends
from fastapi.security import APIKeyCookie

from src.core.config import settings
from src.core.exceptions import Unauthorized
from src.core.redis import get_redis

api_key_cookie = APIKeyCookie(name=settings.session.SESSION_ID)


async def get_current_user(session_id: str = Depends(api_key_cookie)):
    redis = get_redis()
    if not session_id:
        raise Unauthorized(status_code=401, detail="You are not logged in")
    session = await redis.get(session_id)
    if not session:
        raise Unauthorized(status_code=401, detail="You are not logged in")
    return session
