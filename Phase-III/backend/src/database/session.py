from sqlmodel import create_engine, Session
from typing import Generator
from .config import settings


# Create engine with settings from config
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,  # Set to True to see SQL queries in logs
    pool_pre_ping=True,  # Verify connections before use
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    """
    with Session(engine) as session:
        yield session