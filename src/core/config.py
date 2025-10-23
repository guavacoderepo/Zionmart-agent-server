from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",             # load from .env file
        env_file_encoding="utf-8",   # encoding
        extra="ignore"               # ignore unknown env vars
    )

    # General
    APP_NAME: str = "Agentic Customer Care Service"
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str

    # LLM / API Keys
    GOOGLE_API_KEY: str | None