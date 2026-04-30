from fastapi import Request, Depends

from src.core.exceptions import Unauthorized
from src.core.redis import RedisClient


async def get_redis() -> RedisClient:
    return RedisClient()


async def get_current_user(request: Request, redis: RedisClient = Depends(get_redis)):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise Unauthorized(status_code=401, detail="You are not logged in")
    session = await redis.get(session_id)
    if not session:
        raise Unauthorized(status_code=401, detail="You are not logged in")
    return session
