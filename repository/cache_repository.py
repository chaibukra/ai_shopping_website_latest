from typing import Optional
from redisClient.redis_client import redis_client
from config.config import Config

config = Config()


async def create_cache_entity(key: str, value: str):
    if not await redis_client.exists(key):
        await redis_client.setex(key, config.REDIS_TTL, value)


async def get_cache_entity(key: str) -> Optional[str]:
    if await redis_client.exists(key):
        return await redis_client.get(key)
    else:
        return None


async def update_cache_entity(key: str, value: str):
    if await redis_client.exists(key):
        await redis_client.setx(key, config.REDIS_TTL, value)


async def delete_cache_entity(key: str):
    if await redis_client.exists(key):
        await redis_client.delete(key)


async def is_key_exists(key: str) -> bool:
    return bool(await redis_client.exists(key))
