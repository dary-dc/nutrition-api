from fastapi import APIRouter
from app.routers import auth, foods, meals, home, users

API_PREFIX = "/api/v0"

api_router = APIRouter(prefix=API_PREFIX)

# Register all routers here
api_router.include_router(foods.router, prefix="/foods", tags=["foods"])
api_router.include_router(meals.router, prefix="/meals", tags=["meals"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(auth.router, prefix="/users", tags=["users"])

# Optionally register home outside this prefix
root_router = APIRouter()
root_router.include_router(home.router, tags=["home"])
