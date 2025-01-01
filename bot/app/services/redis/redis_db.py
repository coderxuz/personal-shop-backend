import redis.asyncio as redis
from redis.asyncio.client import Redis

from backend.common import REDIS_URL

if not REDIS_URL:
    raise ValueError("REDIS_URL didn't find")


async def get_redis():
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)  # type:ignore
    return redis_client


async def set_user_language_redis(redis_client: Redis, user_id: int, lang_code: str):
    """Save the user's language preference in Redis asynchronously"""
    await redis_client.set(f"user:{user_id}:lang", lang_code)


async def get_user_language_redis(redis_client: Redis, user_id: int):
    """Retrieve the user's language preference from Redis asynchronously"""
    lang = await redis_client.get(f"user:{user_id}:lang")

    return lang or None  # Default to "en" if no language is set
