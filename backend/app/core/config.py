"""Application settings loaded from environment variables."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Pydantic settings for ASAAS backend."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://asaas:asaas_password@db:5432/asaas"
    SECRET_KEY: str = "change_me"
    ALGORITHM: str = "HS256"

    REDIS_URL: str = "redis://redis:6379"

    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "asaas"
    MINIO_SECRET_KEY: str = "asaas123456"

    AI_PROVIDER: str = "disabled"  # disabled | ollama | openai


settings = Settings()
