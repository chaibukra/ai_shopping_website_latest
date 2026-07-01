from typing import Optional
from redisClient.redis_client import redis_client
from config.config import Config
from datetime import datetime, timedelta

config = Config()

redis_available = True
redis_next_retry = datetime.min


def redis_guard(default_return=None):
    def decorator(func):

        async def wrapper(*args, **kwargs):
            global redis_available, redis_next_retry

            if not redis_available:
                if datetime.now() < redis_next_retry:
                    return default_return

                redis_available = True

            try:
                return await func(*args, **kwargs)

            except Exception:
                redis_available = False
                redis_next_retry = datetime.now() + timedelta(seconds=30)
                return default_return

        return wrapper

    return decorator


@redis_guard(default_return=None)
async def create_cache_entity(key: str, value: str):
    if not await redis_client.exists(key):
        await redis_client.setex(key, config.REDIS_TTL, value)


@redis_guard(default_return=None)
async def get_cache_entity(key: str) -> Optional[str]:
    return await redis_client.get(key)


@redis_guard(default_return=None)
async def update_cache_entity(key: str, value: str):
    await redis_client.setex(key, config.REDIS_TTL, value)


@redis_guard(default_return=None)
async def delete_cache_entity(key: str):
    await redis_client.delete(key)


@redis_guard(default_return=False)
async def is_key_exists(key: str) -> bool:
    return bool(await redis_client.exists(key))

