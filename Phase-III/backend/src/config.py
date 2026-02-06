"""
Configuration settings for the Todo AI Agent
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql+asyncpg://username:password@localhost/todo_db"

    # OpenAI settings
    openai_api_key: str

    # MCP Server settings
    mcp_server_url: str = "http://localhost:8001"

    # Application settings
    app_env: str = "development"
    log_level: str = "INFO"

    # JWT settings for authentication
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"


# Create a single instance of settings
settings = Settings()