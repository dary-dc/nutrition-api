from fastapi import FastAPI
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.exceptions import RateLimitException

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(RateLimitExceeded)
    def rate_limit_handler(request, exc):
        return RateLimitException()
