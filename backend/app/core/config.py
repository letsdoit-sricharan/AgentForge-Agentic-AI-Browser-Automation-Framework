from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Application-wide configuration, loaded from environment variables
    and the ``.env`` file at the project root.
    """

    # -----------------------------------------------------------------------
    # Application
    # -----------------------------------------------------------------------
    APP_NAME: str = "AgentForge"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # -----------------------------------------------------------------------
    # Server
    # -----------------------------------------------------------------------
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # -----------------------------------------------------------------------
    # CORS
    # Comma-separated list of allowed origins.
    # Default allows localhost dev servers for React/Vite/Next.js frontends.
    # -----------------------------------------------------------------------
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
    ]

    # -----------------------------------------------------------------------
    # Database
    # -----------------------------------------------------------------------
    DATABASE_URL: str = "sqlite:///./agentforge.db"

    # -----------------------------------------------------------------------
    # Auth
    # -----------------------------------------------------------------------
    JWT_SECRET_KEY: str = "changeme-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # -----------------------------------------------------------------------
    # LLM / AI
    # -----------------------------------------------------------------------
    OPENAI_API_KEY: str = ""

    # -----------------------------------------------------------------------
    # Browser Engine
    # -----------------------------------------------------------------------
    BROWSER_NAME: str = "chromium"
    HEADLESS: bool = True
    BROWSER_TIMEOUT: int = 30000

    # -----------------------------------------------------------------------
    # Logging
    # -----------------------------------------------------------------------
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
