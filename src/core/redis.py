from functools import lru_cache

from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError, TimeoutError as RedisTimeoutError

from src.core.config import settings
from src.core.logging_app import get_logger


logger = get_logger(__name__)


@lru_cache
def get_redis() -> Redis:
    return Redis.from_url(
        url=settings.redis_settings.REDIS_URL,
        max_connections=settings.redis_settings.CONNECTION_POOL_MAXSIZE,
        decode_responses=True,
    )


class RedisClient:
    def __init__(self):
        self._redis = get_redis()

    async def __aenter__(self):
        self.redis = self._redis
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.redis.aclose()

    async def set(self, key: str, value) -> bool:
        try:
            await self.redis.set(key, value, ex=settings.redis_settings.EXPIRE)
            logger.info("redis_set", key=key)
            return True
        except (RedisConnectionError, RedisTimeoutError) as e:
            logger.error("Redis connection error", error=str(e))
            return False
        except Exception as e:
            logger.error("Redis set operation failed", key=key, error=str(e))
            raise e

    async def get(self, key: str) -> str | bool:
        try:
            value = await self.redis.get(key)
            if value:
                logger.info("redis_get", key=key)
                return value
            else:
                return "Does not exist"
        except (RedisConnectionError, RedisTimeoutError) as e:
            logger.error("Redis connection error", error=str(e))
            return False
        except Exception as e:
            logger.error("Redis get operation failed", key=key, error=str(e))
            raise e

    async def expire(self, key: str) -> bool:
        try:
            await self.redis.expire(key, settings.redis_settings.EXPIRE)
            logger.info("redis_expire", key=key)
            return True
        except (RedisConnectionError, RedisTimeoutError) as e:
            logger.error("Redis connection error", error=str(e))
            return False
        except Exception as e:
            logger.error("Redis expire operation failed", key=key, error=str(e))
            raise e

    async def delete(self, key: str) -> bool:
        try:
            await self.redis.delete(key)
            logger.info("redis_delete", key=key)
            return True
        except (RedisConnectionError, RedisTimeoutError) as e:
            logger.error("Redis connection error", error=str(e))
            return False
        except Exception as e:
            logger.error("Redis delete operation failed", key=key, error=str(e))
            raise e
