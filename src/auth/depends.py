from fastapi import Request

from src.core.exceptions import Unauthorized
from src.core.redis import get_redis


async def get_current_user(request: Request):
    redis = get_redis()
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise Unauthorized(status_code=401, detail="You are not logged in")
    session = await redis.get(session_id)
    if not session:
        raise Unauthorized(status_code=401, detail="You are not logged in")
    return session
