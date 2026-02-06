# Quickstart Guide: Chat Flow & API for Stateless Todo Assistant

## Prerequisites

- Python 3.9+
- PostgreSQL-compatible database (Neon recommended)
- OpenAI API key
- MCP server running with task tools

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Update the following variables in .env:
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=your_postgres_connection_string
MCP_SERVER_URL=http://localhost:8001
BETTER_AUTH_SECRET=your_auth_secret_here
BETTER_AUTH_URL=http://localhost:3000
```

### 2. Database Setup
```bash
# Install dependencies
pip install sqlmodel alembic psycopg2-binary

# Run database migrations
alembic upgrade head
```

### 3. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload --port 8000
```

## Running the Chat API

### 1. Starting the Server
```bash
# Navigate to backend directory
cd backend

# Start the chat API server
uvicorn src.main:app --reload --port 8000
```

### 2. API Usage Examples

#### Basic Chat Request
```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

#### Continuing a Conversation
```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_456789",
    "message": "What tasks do I have?"
  }'
```

### 3. Expected Responses
- Successful response: Contains conversation_id, response text, and tool_calls
- Error responses: Proper error messages with status codes

## Testing the Chat API

### Running Unit Tests
```bash
# Run unit tests for chat API
pytest tests/unit/test_chat_api.py
```

### Running Integration Tests
```bash
# Run integration tests
pytest tests/integration/test_chat_integration.py
```

## Troubleshooting

### Common Issues
- **MCP Server Not Responding**: Verify MCP server is running on configured URL
- **Database Connection Issues**: Check DATABASE_URL in environment variables
- **Authentication Errors**: Verify JWT token validity and user permissions
- **OpenAI API Issues**: Confirm API key is valid and has sufficient quota

### Logs
- API server logs: Check console output from FastAPI server
- Error logs: Located in logs/chat_api.log
- Conversation logs: Track conversation flow and tool usage