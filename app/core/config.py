from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database
    DATABASE_URL: str
    DEV_DATABASE_URL: str
    TEST_DATABASE_URL: str | None = None

    # Environment
    ENVIRONMENT: str = "local"
    DEBUG: bool = True

    # Cache
    CACHE_BACKEND: str
    CACHE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
