from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def remove_database_file():

    url = get_database_url()
    if not url.startswith('sqlite'):
        return
    
    print("Deleting previous database file for development")

    file = url.split('/')[-1]

    import os
    if os.path.exists(file):
        os.remove(file)
    


def get_database_url() -> str:
    if settings.ENVIRONMENT in ["local"]:
        return settings.DEV_DATABASE_URL
    return settings.DATABASE_URL

def get_connect_args() -> dict:
    if settings.ENVIRONMENT in ["local"]:
        return {"check_same_thread": False}
    return {}

Base = declarative_base()

engine = create_engine(get_database_url(), connect_args=get_connect_args())


# Enable foreign keys for SQLite
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):

    if settings.ENVIRONMENT not in ["local"]:
        return

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
