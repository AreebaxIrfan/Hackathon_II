from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import API routers
from api.auth import router as auth_router
from api.protected import router as protected_router
from api.tasks_api import router as tasks_api_router

# Load environment variables
load_dotenv()

# Create FastAPI app instance
app = FastAPI(
    title="Task Management API",
    description="API for secure task management with user isolation",
    version="1.0.0"
)

# Add CORS middleware for token-based authentication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Allow authorization header

)

# Include API routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(protected_router, prefix="/api", tags=["protected"])
app.include_router(tasks_api_router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}