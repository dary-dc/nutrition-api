from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis
from fastapi_cache.backends.inmemory import InMemoryBackend


# TODO: add conditional cache using depending on the context
async def init_cache():
    # redis = aioredis.from_url("redis://localhost")
    # FastAPICache.init(RedisBackend(redis), prefix="nutrition-cache")
    FastAPICache.init(InMemoryBackend(), prefix="dev-cache")
