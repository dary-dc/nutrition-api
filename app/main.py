from fastapi import FastAPI, APIRouter
from fastapi.concurrency import asynccontextmanager
from app.core.seed.seed_permissions import seed_permissions
from app.core.seed.seed_roles import seed_roles
from app.core.seed.seed_admin import seed_admin
from app.database import Base, SessionLocal, engine
from app.routers.api import api_router, root_router
from app.core.limiter import register_rate_limiter

# Create DB tables
Base.metadata.create_all(bind=engine)


# TODO: improve implementation
@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_permissions(db)
        seed_roles(db)
        seed_admin(db)
        yield

    finally:
        db.close()


app = FastAPI(
    title="Nutrition API",
    version="0.1.0",
    lifespan=lifespan,
)

# TODO: move to .env?
API_PREFIX = "/api/v0"
api_router = APIRouter(prefix=API_PREFIX)

# Include all routers
app.include_router(api_router)
app.include_router(root_router)

# SlowAPI middleware for ratelimiting and exception handler
register_rate_limiter(app)
