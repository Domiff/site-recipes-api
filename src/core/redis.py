from functools import lru_cache

from redis.asyncio import Redis
from redis.exceptions import (
    ConnectionError as RedisConnectionError,
    TimeoutError as RedisTimeoutError,
)

from src.core.config import settings
from src.core.logging_app import get_logger


logger = get_logger(__name__)


@lru_cache
def get_redis() -> Redis:
    return Redis.from_url(
        url=settings.redis.REDIS_URL,
        max_connections=settings.redis.CONNECTION_POOL_MAXSIZE,
        decode_responses=True,
    )


class RedisClient:
    def __init__(self):
        self.redis = get_redis()

    async def set(self, key: str, value) -> None:
        try:
            await self.redis.set(key, value, ex=settings.redis.EXPIRE)
            logger.info("redis_set", key=key)
        except (RedisConnectionError, RedisTimeoutError) as e:
            logger.error("Redis connection error", error=str(e))
            raise
        except Exception as e:
            logger.error("Redis set operation failed", key=key, error=str(e))
            raise

    async def get(self, key: str) -> str | None:
        try:
            value = await self.redis.get(key)
            if value:
                logger.info("redis_get", key=key)
                return value
            else:
                return None
        except (RedisConnectionError, RedisTimeoutError) as e:
            logger.error("Redis connection error", error=str(e))
            raise
        except Exception as e:
            logger.error("Redis get operation failed", key=key, error=str(e))
            raise

    async def expire(self, key: str) -> None:
        try:
            await self.redis.expire(key, settings.redis.EXPIRE)
            logger.info("redis_expire", key=key)
        except (RedisConnectionError, RedisTimeoutError) as e:
            logger.error("Redis connection error", error=str(e))
            raise
        except Exception as e:
            logger.error("Redis expire operation failed", key=key, error=str(e))
            raise

    async def delete(self, key: str) -> None:
        try:
            await self.redis.delete(key)
            logger.info("redis_delete", key=key)
        except (RedisConnectionError, RedisTimeoutError) as e:
            logger.error("Redis connection error", error=str(e))
            raise
        except Exception as e:
            logger.error("Redis delete operation failed", key=key, error=str(e))
            raise
