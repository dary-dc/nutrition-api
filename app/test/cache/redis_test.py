import asyncio
from redis import asyncio as aioredis


async def test():
    redis = aioredis.from_url("redis://localhost:6379")
    await redis.set("hello", "world")
    print(await redis.get("hello"))


asyncio.run(test())
