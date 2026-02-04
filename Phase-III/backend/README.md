# AI Todo Agent Backend

Backend service for the AI-powered todo assistant that understands natural language and manages tasks by invoking MCP tools.

## Tech Stack

- Python 3.9+
- FastAPI
- SQLModel
- OpenAI API
- PostgreSQL (Neon)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp ../.env.example .env
   # Update the values in .env
   ```

3. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

## API Endpoints

- `POST /api/{user_id}/chat` - Process natural language input and manage tasks

## Architecture

- **Models**: Located in `src/models/` - Define the data structures
- **Services**: Located in `src/services/` - Business logic layer
- **API**: Located in `src/api/v1/` - API endpoints
- **Agents**: Located in `src/agents/` - AI logic
- **Middleware**: Located in `src/middleware/` - Request processing