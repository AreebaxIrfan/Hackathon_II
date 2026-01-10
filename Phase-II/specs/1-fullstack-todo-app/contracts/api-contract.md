# API Contract: Full-Stack Todo Web Application

## Overview
This document defines the API contract for the Full-Stack Todo Web Application, specifying the endpoints, request/response formats, authentication requirements, and error handling.

## Base URL
```
https://api.yourdomain.com/api
```
Or for development:
```
http://localhost:8000/api
```

## Authentication
All endpoints require JWT authentication via the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## Common Headers
- `Content-Type: application/json`
- `Authorization: Bearer <jwt_token>` (for authenticated endpoints)

## Common Error Responses

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

## Endpoints

### Authentication Endpoints

#### POST /auth/register
Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "confirmPassword": "secure_password"
}
```

**Response (201 Created)**:
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "createdAt": "2023-01-01T00:00:00Z"
}
```

**Response (400 Bad Request)**:
```json
{
  "detail": "Email already registered"
}
```

#### POST /auth/login
Login with existing credentials.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  }
}
```

#### POST /auth/logout
Logout current user.

**Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

### Task Management Endpoints

#### GET /tasks
Retrieve all tasks for the authenticated user.

**Query Parameters**:
- `completed` (optional): Filter by completion status (true/false)
- `limit` (optional): Limit number of results (default: 50, max: 100)
- `offset` (optional): Offset for pagination (default: 0)

**Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Sample Task",
      "description": "Description of the task",
      "completed": false,
      "userId": "user-uuid-string",
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

#### POST /tasks
Create a new task for the authenticated user.

**Request Body**:
```json
{
  "title": "New Task",
  "description": "Description of the new task",
  "completed": false
}
```

**Response (201 Created)**:
```json
{
  "id": "uuid-string",
  "title": "New Task",
  "description": "Description of the new task",
  "completed": false,
  "userId": "user-uuid-string",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

#### GET /tasks/{id}
Retrieve a specific task by ID.

**Path Parameters**:
- `id`: Task ID (UUID string)

**Response (200 OK)**:
```json
{
  "id": "uuid-string",
  "title": "Sample Task",
  "description": "Description of the task",
  "completed": false,
  "userId": "user-uuid-string",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

#### PUT /tasks/{id}
Update an existing task.

**Path Parameters**:
- `id`: Task ID (UUID string)

**Request Body**:
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "id": "uuid-string",
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true,
  "userId": "user-uuid-string",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-02T00:00:00Z"
}
```

#### DELETE /tasks/{id}
Delete a specific task.

**Path Parameters**:
- `id`: Task ID (UUID string)

**Response (204 No Content)**:
```
No content returned
```

#### PATCH /tasks/{id}/complete
Toggle the completion status of a task.

**Path Parameters**:
- `id`: Task ID (UUID string)

**Request Body**:
```json
{
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "id": "uuid-string",
  "title": "Sample Task",
  "description": "Description of the task",
  "completed": true,
  "userId": "user-uuid-string",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-02T00:00:00Z"
}
```

## Data Models

### User
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

### Task
```json
{
  "id": "uuid-string",
  "title": "Task Title",
  "description": "Task description",
  "completed": false,
  "userId": "user-uuid-string",
  "createdAt": "2023-01-01T00:00:00Z",
  "updatedAt": "2023-01-01T00:00:00Z"
}
```

## Security Considerations

1. All endpoints require valid JWT authentication
2. Users can only access their own resources
3. All inputs are validated to prevent injection attacks
4. Passwords are never exposed in API responses
5. Error messages don't reveal sensitive system information