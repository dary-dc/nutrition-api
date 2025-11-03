from fastapi import FastAPI, APIRouter
from app.database import Base, engine
from app.routers import foods, meals, auth, home
from app.core.limiter import register_rate_limiter

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

# SlowAPI middleware for ratelimiting and exception handler
register_rate_limiter(app)