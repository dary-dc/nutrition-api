from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.core.config import settings


async def init_cache() -> None:
    """
    Initialize FastAPI-Cache with either Redis or in-memory backend,
    depending on configuration and environment.
    """

    backend = (settings.CACHE_BACKEND or "auto").lower()
    env = (settings.ENVIRONMENT or "local").lower()

    use_redis = backend == "redis" or (
        backend == "auto" and env not in ["local", "test"]
    )

    if use_redis:
        try:
            redis = aioredis.from_url(
                settings.CACHE_URL,
                encoding="utf-8",
                decode_responses=True,
            )
            FastAPICache.init(RedisBackend(redis), prefix="api")
            print(f"✅ Cache initialized with Redis backend at {settings.CACHE_URL}")
        except Exception as e:
            # Graceful fallback to in-memory cache if Redis fails
            FastAPICache.init(InMemoryBackend(), prefix="fallback-api")
            print(f"⚠️ Redis connection failed ({e}); using in-memory cache instead.")
    else:
        FastAPICache.init(InMemoryBackend(), prefix="dev-api")
        print("⚙️ Cache initialized with In-Memory backend (DEV mode)")
