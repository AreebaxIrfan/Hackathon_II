from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database settings
    DATABASE_URL: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    # Application settings
    APP_NAME: str = "Full-Stack Web Application"
    DEBUG: bool = False
    VERSION: str = "1.0.0"

    # CORS settings
    FRONTEND_URL: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()