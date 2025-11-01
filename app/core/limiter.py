from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.exceptions import RateLimitException

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


def register_rate_limiter(app: FastAPI):
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return RateLimitException()

    app.state.limiter = limiter
    app.add_middleware(limiter)
