from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db_and_tables
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    await create_db_and_tables()
    yield


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Todo Agent API",
    description="API for the AI-powered todo assistant that understands natural language and manages tasks by invoking MCP tools.",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routes after app creation to avoid circular imports
from .api.v1.chat import router as chat_router
from .api.auth_routes import router as auth_router
from .api.todo_routes import router as todo_router

app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(todo_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the AI Todo Agent API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}