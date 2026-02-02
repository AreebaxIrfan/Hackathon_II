# API Contracts: Multi-user Todo Web Application

## Overview
REST API contracts for the secure, multi-user todo web application with JWT authentication and user data isolation.

## Base Configuration
- **Base URL**: `/api`
- **Authentication**: JWT Bearer token required for all endpoints (except auth endpoints)
- **Headers**:
  - `Authorization: Bearer <jwt_token>` for authenticated requests
  - `Content-Type: application/json` for requests with body

## Endpoints

### Authentication Endpoints
These endpoints do NOT require authentication:

#### POST /auth/register
- **Description**: Register a new user account
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```
- **Response**: 200 OK with user information
- **Error Responses**: 400 Bad Request for validation errors, 409 Conflict for duplicate email

#### POST /auth/login
- **Description**: Authenticate user and return JWT token
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```
- **Response**: 200 OK with JWT token
- **Error Responses**: 400 Bad Request, 401 Unauthorized for invalid credentials

#### POST /auth/logout
- **Description**: Logout user and invalidate session
- **Request Body**: None
- **Response**: 200 OK
- **Error Responses**: 401 Unauthorized for invalid token

### Task Management Endpoints
These endpoints require valid JWT authentication:

#### GET /api/tasks
- **Description**: List authenticated user's tasks
- **Query Parameters**:
  - `status`: pending|completed|all (default: all)
  - `sort`: created|title|-created (negative = descending, default: -created)
- **Response**: 200 OK with array of tasks
  ```json
  [
    {
      "id": "task-uuid",
      "title": "Sample task",
      "description": "Task description",
      "completed": false,
      "created_at": "2026-01-11T10:00:00Z",
      "updated_at": "2026-01-11T10:00:00Z"
    }
  ]
  ```
- **Error Responses**: 401 Unauthorized for missing/invalid token

#### POST /api/tasks
- **Description**: Create a new task for authenticated user
- **Request Body**:
  ```json
  {
    "title": "New task",
    "description": "Task description",
    "completed": false
  }
  ```
- **Response**: 201 Created with created task
- **Error Responses**: 400 Bad Request for validation errors, 401 Unauthorized for invalid token

#### GET /api/tasks/{task_id}
- **Description**: Get a specific task by ID
- **Response**: 200 OK with task details
- **Error Responses**: 401 Unauthorized, 403 Forbidden for other user's task, 404 Not Found

#### PUT /api/tasks/{task_id}
- **Description**: Update a specific task by ID
- **Request Body**:
  ```json
  {
    "title": "Updated task",
    "description": "Updated description",
    "completed": true
  }
  ```
- **Response**: 200 OK with updated task
- **Error Responses**: 400 Bad Request, 401 Unauthorized, 403 Forbidden for other user's task, 404 Not Found

#### DELETE /api/tasks/{task_id}
- **Description**: Delete a specific task by ID
- **Response**: 204 No Content
- **Error Responses**: 401 Unauthorized, 403 Forbidden for other user's task, 404 Not Found

#### PATCH /api/tasks/{task_id}/complete
- **Description**: Toggle completion status of a specific task
- **Request Body**:
  ```json
  {
    "completed": true
  }
  ```
- **Response**: 200 OK with updated task
- **Error Responses**: 400 Bad Request, 401 Unauthorized, 403 Forbidden for other user's task, 404 Not Found

## Authentication & Security
- All task endpoints require valid JWT in Authorization header
- 401 Unauthorized: Missing/invalid/expired token
- 403 Forbidden: Token valid but user not authorized for resource
- Every task query must filter WHERE user_id = decoded JWT subject
- Task ownership enforced on create/update/delete operations

## Error Response Format
```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2026-01-11T10:00:00Z"
}
```