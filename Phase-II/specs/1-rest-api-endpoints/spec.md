# Feature Specification: REST API Endpoints

**Feature Branch**: `1-rest-api-endpoints`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "/sp.specify (REST API Endpoints)
Focus

Define secure, RESTful API endpoints for task management with JWT-based authentication.

Success Criteria (4)

All task-related endpoints follow REST conventions.

Every API request requires a valid JWT token.

Endpoints return correct HTTP status codes and JSON responses.

API only exposes tasks belonging to the authenticated user.

Constraints (4)

All routes must be prefixed with /api/.

Backend must only verify JWT, not manage auth sessions.

User identity must be derived from JWT, not request body.

API must be implemented using FastAPI conventions.

Not Building (4)

No GraphQL or RPC-style APIs.

No public or unauthenticated endpoints.

No versioning system (e.g., /v1, /v2).

No rate limiting or API analytics."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Creation via API (Priority: P1)

Authenticated user makes a POST request to create a new task through the API. The system validates the JWT token, extracts user identity from the token, creates the task linked to the user, and returns the created task in JSON format with a 201 status code.

**Why this priority**: Essential functionality for the task management system - users need to be able to create tasks to have any value from the system.

**Independent Test**: Can be fully tested by making a POST request to /api/tasks with a valid JWT token and task data, and delivers the ability for authenticated users to create tasks.

**Acceptance Scenarios**:

1. **Given** user has a valid JWT token, **When** user sends POST request to /api/tasks with valid task data, **Then** system creates task linked to user identity and returns 201 Created with task JSON
2. **Given** user has invalid/expired JWT token, **When** user sends POST request to /api/tasks, **Then** system returns 401 Unauthorized

---

### User Story 2 - Task Retrieval via API (Priority: P1)

Authenticated user makes a GET request to retrieve their tasks through the API. The system validates the JWT token, extracts user identity from the token, retrieves only tasks belonging to that user, and returns the tasks in JSON format.

**Why this priority**: Essential functionality for the task management system - users need to be able to view their tasks to manage them effectively.

**Independent Test**: Can be fully tested by making a GET request to /api/tasks with a valid JWT token, and delivers the ability for authenticated users to view their own tasks.

**Acceptance Scenarios**:

1. **Given** user has a valid JWT token, **When** user sends GET request to /api/tasks, **Then** system returns only tasks belonging to the user in JSON format with 200 OK
2. **Given** user has invalid/expired JWT token, **When** user sends GET request to /api/tasks, **Then** system returns 401 Unauthorized

---

### User Story 3 - Individual Task Operations via API (Priority: P2)

Authenticated user makes requests to retrieve, update, or delete a specific task through the API. The system validates the JWT token, extracts user identity, ensures the task belongs to the user, and performs the requested operation.

**Why this priority**: Important for complete task lifecycle management, allowing users to modify and manage individual tasks.

**Independent Test**: Can be fully tested by making GET, PUT, PATCH, or DELETE requests to /api/tasks/{id} with a valid JWT token, and delivers the ability for authenticated users to manage individual tasks.

**Acceptance Scenarios**:

1. **Given** user has a valid JWT token and owns the task, **When** user sends GET request to /api/tasks/{id}, **Then** system returns the specific task in JSON format with 200 OK
2. **Given** user has a valid JWT token but doesn't own the task, **When** user sends GET request to /api/tasks/{id}, **Then** system returns 404 Not Found
3. **Given** user has a valid JWT token and owns the task, **When** user sends PUT request to /api/tasks/{id} with updated data, **Then** system updates the task and returns 200 OK with updated task JSON

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST validate JWT tokens on every API request to /api/ endpoints
- **FR-002**: System MUST extract user identity from JWT claims, not from request body or headers other than Authorization
- **FR-003**: System MUST ensure all API routes are prefixed with /api/
- **FR-004**: System MUST only return tasks that belong to the authenticated user making the request
- **FR-005**: System MUST return JSON responses for all API endpoints
- **FR-006**: System MUST return appropriate HTTP status codes (200, 201, 401, 403, 404, etc.) based on request outcome
- **FR-007**: System MUST follow REST conventions for HTTP methods (GET, POST, PUT, PATCH, DELETE)
- **FR-008**: System MUST verify JWT tokens without managing authentication sessions
- **FR-009**: System MUST implement the API using FastAPI conventions and patterns

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with attributes like title, description, completion status, and creation date. Associated with a specific user through user identity derived from JWT.
- **JWT Token**: Authentication token containing user identity claims that must be validated for all API requests.
- **User Identity**: Information extracted from JWT token that determines which tasks a user can access.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API endpoints follow REST conventions with 100% adherence to standard HTTP methods and URL patterns
- **SC-002**: Every API request requires a valid JWT token with 100% enforcement rate
- **SC-003**: All API endpoints return correct HTTP status codes and JSON responses with 100% accuracy
- **SC-004**: API only exposes tasks belonging to the authenticated user with 0% cross-user data leakage
- **SC-005**: All routes are prefixed with /api/ with 100% compliance
- **SC-006**: System achieves 99% uptime for authenticated API requests during normal operating hours