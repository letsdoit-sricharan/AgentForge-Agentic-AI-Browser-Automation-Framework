"""
Application configuration.

This module provides a centralized configuration system for the
AgentForge backend using Pydantic Settings.

All environment variables must be accessed through the Settings
instance defined in this module.
"""
from pathlib import Path
"""it always finds the .env file, regardless of where you run the application from."""
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application settings.

    Values are automatically loaded from the .env file
    and validated during application startup.
    """

    # -------------------------------------------------
    # Application
    # -------------------------------------------------

    APP_NAME: str = "AgentForge"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # -------------------------------------------------
    # Server
    # -------------------------------------------------

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # -------------------------------------------------
    # Database
    # -------------------------------------------------

    DATABASE_URL: str

    # -------------------------------------------------
    # Authentication
    # -------------------------------------------------

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # -------------------------------------------------
    # OpenAI
    # -------------------------------------------------

    OPENAI_API_KEY: str = ""

    # -------------------------------------------------
    # Browser
    # -------------------------------------------------

    BROWSER_NAME: str = "chromium"
    HEADLESS: bool = False
    BROWSER_TIMEOUT: int = 30000

    # -------------------------------------------------
    # Logging
    # -------------------------------------------------

    LOG_LEVEL: str = "INFO"

BASE_DIR = Path(__file__).resolve().parent.parent.parent

model_config = SettingsConfigDict(
    env_file=BASE_DIR / ".env",
    case_sensitive=True,
    extra="ignore",
)


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    Ensures the configuration is loaded only once
    during the application lifecycle.
    """
    return Settings()


settings = get_settings()