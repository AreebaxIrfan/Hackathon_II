# Quickstart Guide: Todo Application with AI Chat

**Feature**: 001-validation-spec
**Date**: 2026-02-05

## Overview
This guide will help you set up and run the Todo Full-Stack Application with conversational AI interface.

## Prerequisites
- Node.js 18+ installed
- Python 3.11+ installed
- PostgreSQL or Neon PostgreSQL account
- OpenAI API key
- Git

## Setup Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Update environment variables in .env.local
OPENAI_API_KEY=your_openai_api_key_here
BACKEND_URL=http://localhost:8000
```

### 3. Backend Setup
```bash
# Navigate to backend directory
cd ../backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Update environment variables in .env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
NEON_DB_URL=your_neon_database_url
MCP_SECRET_KEY=your_mcp_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
```

### 4. Database Setup
```bash
# Make sure you're in the backend directory
cd src

# Run database migrations
python -m alembic upgrade head

# Or initialize the database directly if using SQLModel
python -m scripts.init_db
```

### 5. Running the Application

#### Option A: Separate Terminals
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
npm run dev
```

#### Option B: Using Docker Compose (if available)
```bash
docker-compose up --build
```

### 6. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Documentation: http://localhost:8000/docs

## Directory Structure
```
project-root/
├── backend/
│   ├── src/
│   │   ├── models/     # SQLModel database models
│   │   ├── services/   # Business logic
│   │   ├── api/        # API routes
│   │   ├── mcp/        # MCP server implementation
│   │   └── agents/     # OpenAI agent integration
│   └── tests/
├── frontend/
│   ├── app/            # Next.js 14 App Router
│   │   ├── components/ # Reusable UI components
│   │   ├── lib/        # Utilities and helpers
│   │   └── chat/       # Chat interface components
│   └── tests/
└── specs/
    └── 001-validation-spec/
```

## Key Features Setup

### Chat Interface
- The chat interface is integrated on the main Todo page
- It connects to the backend chat endpoint at `/api/v1/chat`
- Messages are persisted in the database for continuity

### MCP Server
- The MCP server is available at `/mcp/tools`
- Exposes Todo operations as tools for the AI agent
- Remains stateless with all data persisted in the database

### Authentication
- User authentication is required for Todo operations
- JWT tokens are used for API authentication
- Tokens are securely stored in the frontend

## Troubleshooting

### Common Issues
1. **Port already in use**: Change port numbers in start commands
2. **Database connection errors**: Verify DATABASE_URL is correct
3. **API key issues**: Check that OPENAI_API_KEY is properly set
4. **Frontend-backend communication**: Verify BACKEND_URL matches running backend

### Verification Steps
```bash
# Verify backend is running
curl http://localhost:8000/health

# Verify database connectivity
python -c "import sqlmodel; print('Database connection successful')"

# Check if frontend can reach backend
curl http://localhost:8000/api/v1/health
```

## Development Commands

### Backend
```bash
# Run tests
pytest tests/

# Run with debugging
python -m debugpy --listen 5678 src/main.py

# Format code
black src/
```

### Frontend
```bash
# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint
```

## Next Steps
1. Verify the application loads correctly in the browser
2. Create an account and log in
3. Test creating and managing todos
4. Interact with the chatbot to manage tasks
5. Verify all functionality works as specified in the feature requirements