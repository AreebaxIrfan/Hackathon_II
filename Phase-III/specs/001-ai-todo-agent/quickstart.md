# Quickstart Guide: AI Todo Agent

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL-compatible database (Neon recommended)
- OpenAI API key
- Better Auth compatible environment

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Update the following variables in .env:
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_postgres_connection_string
BETTER_AUTH_SECRET=your_auth_secret
BETTER_AUTH_URL=http://localhost:3000
```

### 2. Database Setup
```bash
# Install dependencies
pip install sqlmodel alembic psycopg2-binary

# Run database migrations
alembic upgrade head
```

### 3. MCP Server Setup
```bash
# Navigate to MCP server directory
cd mcp-server

# Install Python dependencies
pip install -r requirements.txt

# Start MCP server
python -m mcp_server.main
```

### 4. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload --port 8000
```

### 5. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```

## Running the Application

1. Start the MCP server: `python -m mcp_server.main`
2. Start the backend: `uvicorn main:app --port 8000`
3. Start the frontend: `npm run dev`
4. Access the application at `http://localhost:3000`

## Testing the AI Agent

### Natural Language Commands Supported
- "Add a task to buy groceries" → Creates new task
- "Show my tasks" → Lists all tasks
- "What's pending?" → Lists incomplete tasks
- "Mark task 3 as complete" → Marks task as completed
- "Delete the meeting task" → Lists tasks first, then deletes if ambiguous

### API Testing
```bash
# Send a test request to the chat endpoint
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

## Troubleshooting

### Common Issues
- **MCP Server Not Responding**: Verify the MCP server is running and accessible
- **Database Connection Issues**: Check DATABASE_URL in environment variables
- **Authentication Errors**: Ensure JWT tokens are properly configured
- **AI Agent Not Responding**: Verify OpenAI API key is valid and has sufficient quota

### Logs
- Backend logs: Check console output from uvicorn
- MCP server logs: Check console output from MCP server
- Frontend logs: Check browser console