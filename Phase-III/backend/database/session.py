from sqlmodel import create_engine, Session
from typing import Generator
from dotenv import load_dotenv
import os
from contextlib import contextmanager

# Load environment variables
load_dotenv()

# Get database URL from environment, with a default for testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./task.db")

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.
    """
    with Session(engine) as session:
        yield session