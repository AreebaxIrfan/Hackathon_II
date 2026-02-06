from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./todo_app.db"  # Default to SQLite for development
    db_echo: bool = False  # Set to True to see SQL queries in logs
    db_pool_size: int = 5
    db_max_overflow: int = 10
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()