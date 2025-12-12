"""Application configuration."""
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "Arkhon Integration Platform"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # File Storage
    STORAGE_TYPE: str = "local"  # local, s3
    LOCAL_STORAGE_PATH: str = "./storage"
    S3_BUCKET: Optional[str] = None
    S3_REGION: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    # FTP Settings (BigBuy example)
    BIGBUY_FTP_HOST: Optional[str] = None
    BIGBUY_FTP_PORT: int = 21
    BIGBUY_FTP_USER: Optional[str] = None
    BIGBUY_FTP_PASSWORD: Optional[str] = None
    BIGBUY_FTP_PATH: str = "/products"

    # Import Settings
    CSV_CHUNK_SIZE: int = 1000
    MAX_IMPORT_ERRORS: int = 100

    # Outbound Sync
    OUTBOUND_RETRY_ATTEMPTS: int = 3
    OUTBOUND_RETRY_DELAY: int = 5

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json or text

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
