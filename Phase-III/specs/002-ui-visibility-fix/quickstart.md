# Quickstart Guide: UI Visibility Fix for Chatbot Interface

## Prerequisites

- Node.js 18+ with npm/yarn/pnpm
- Python 3.9+ with pip
- Access to OpenAI API key
- Access to MCP server with task tools running

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Update the following variables in .env:
REACT_APP_API_BASE_URL=your_backend_api_base_url
REACT_APP_OPENAI_API_KEY=your_openai_api_key
REACT_APP_MCP_SERVER_URL=your_mcp_server_url
REACT_APP_BETTER_AUTH_URL=your_auth_url
```

### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Backend Setup (if needed for testing)
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn src.main:app --reload --port 8000
```

## Testing the UI Fix

### 1. Basic UI Visibility Test
1. Navigate to the application in your browser
2. Verify that the chat interface renders completely:
   - Chat window is visible
   - Message history area is visible
   - Input box for typing messages is visible
   - Any initial welcome messages are displayed

### 2. Functionality Test
1. Type a message in the input field
2. Submit the message
3. Verify that:
   - Your message appears in the chat window
   - The AI assistant responds appropriately
   - Response appears in the chat window

### 3. Error Handling Test
1. Test with invalid API configuration (temporarily change in .env)
2. Verify that visible error messages appear instead of blank screens
3. Restore correct configuration and verify UI recovers

## Troubleshooting Common Issues

### UI Not Loading
- Check browser console for JavaScript errors
- Verify ChatKit components are properly initialized
- Ensure API endpoints are correctly configured
- Confirm authentication is not blocking UI rendering

### API Connection Issues
- Verify API endpoint URLs are correct
- Check that backend services are running
- Confirm API authentication is properly configured
- Test API endpoints directly using tools like curl or Postman

### Authentication Blocking UI
- Ensure authentication logic runs after UI initialization
- Check that auth providers are properly configured
- Verify authentication state doesn't prevent UI rendering
- Look for any auth-related error messages in console

## Integration Scenarios

### With Backend Services
- UI connects to `/api/{user_id}/chat` endpoint
- Messages are processed by OpenAI Agent with MCP tools
- Conversation history is maintained across sessions

### With MCP Tools
- UI enables natural language commands that trigger MCP tool calls
- Tool results are displayed in the chat interface
- User isolation is maintained through authentication

### With Authentication
- User identity is established without blocking UI
- Session management happens transparently
- User data isolation is maintained throughout the session