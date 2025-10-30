from fastapi import FastAPI, APIRouter
from app.database import Base, engine
from app.routers import foods, meals, auth, home
from app.core.limiter import limiter, rate_limit_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nutrition API", version="0.1.0")

# TODO: move to .env
API_PREFIX = "/api/v0"
api_router = APIRouter(prefix=API_PREFIX)

# Routers
api_router.include_router(foods.router, prefix="/foods", tags=["foods"])
api_router.include_router(meals.router, prefix="/meals", tags=["meals"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

app.include_router(api_router)
app.include_router(home.router, tags=["home"])

# SlowAPI middleware for ratelimiting
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
