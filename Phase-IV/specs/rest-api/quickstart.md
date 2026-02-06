# Quickstart Guide for Task Management API

## Prerequisites
- Python 3.7+
- pip package manager
- Virtual environment (recommended)

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your SECRET_KEY and other configurations
   ```

3. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

## API Authentication
All API endpoints require JWT authentication. Obtain a token by authenticating with the `/auth/login` endpoint, then include it in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Available Endpoints

### Create a Task
```
POST /api/tasks
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Sample Task",
  "description": "Task description",
  "priority": 3
}
```

### Get User's Tasks
```
GET /api/tasks
Authorization: Bearer <token>
```

Query parameters:
- `completed`: all|pending|completed (default: all)
- `limit`: number of results (default: 50)
- `offset`: pagination offset (default: 0)
- `priority`: filter by priority (1-5)

### Get Specific Task
```
GET /api/tasks/{task_id}
Authorization: Bearer <token>
```

### Update a Task
```
PUT /api/tasks/{task_id}
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Updated Task Title",
  "completed": true
}
```

### Delete a Task
```
DELETE /api/tasks/{task_id}
Authorization: Bearer <token>
```

### Complete a Task
```
PATCH /api/tasks/{task_id}/complete
Authorization: Bearer <token>
```

### Mark Task as Incomplete
```
PATCH /api/tasks/{task_id}/incomplete
Authorization: Bearer <token>
```

## Error Handling
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid JWT token
- `404 Not Found`: Resource does not exist
- `422 Unprocessable Entity`: Validation error

## Response Format
Successful responses return JSON objects with the following structure:
```json
{
  "id": "uuid-string",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "priority": 3,
  "user_id": "uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```