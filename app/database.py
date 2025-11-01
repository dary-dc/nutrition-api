from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def get_database_url():
    if settings.ENVIRONMENT in ["local"]:
        return settings.DEV_DATABASE_URL
    return settings.DATABASE_URL


Base = declarative_base()

engine = create_engine(get_database_url(), connect_args={"check_same_thread": False})


# Enable foreign keys for SQLite
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    # The name “Local” doesn’t mean local development — it means thread-local (safe to use inside requests).
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
