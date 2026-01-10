# Data Model: Full-Stack Todo Web Application

## Overview
This document defines the data models for the Full-Stack Todo Web Application, including entities, relationships, and validation rules.

## Entity Definitions

### User
Represents an authenticated user with unique identifier, email, and authentication credentials.

**Fields**:
- id (UUID/String): Unique identifier for the user (Primary Key)
- email (String): User's email address (Required, Unique, Valid Email Format)
- password_hash (String): Hashed password for authentication (Required)
- created_at (DateTime): Timestamp when user account was created (Required, Auto-generated)
- updated_at (DateTime): Timestamp when user account was last updated (Required, Auto-generated)
- is_active (Boolean): Whether the account is active (Default: True)

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must be hashed before storage (never store plain text)
- Created_at and updated_at timestamps must be automatically managed

**Relationships**:
- One-to-Many: A user can have many tasks

### Task
Represents a todo item with title, description, completion status, creation timestamp, and user ownership relationship.

**Fields**:
- id (UUID/String): Unique identifier for the task (Primary Key)
- title (String): Title of the task (Required, Max Length: 255)
- description (Text): Detailed description of the task (Optional, Max Length: 1000)
- completed (Boolean): Whether the task is completed (Default: False)
- user_id (UUID/String): Foreign key linking to the user who owns the task (Required)
- created_at (DateTime): Timestamp when task was created (Required, Auto-generated)
- updated_at (DateTime): Timestamp when task was last updated (Required, Auto-generated)

**Validation Rules**:
- Title is required and cannot be empty
- Title must not exceed 255 characters
- Description, if provided, must not exceed 1000 characters
- User_id must reference an existing user
- Completed status can be toggled by the task owner

**Relationships**:
- Many-to-One: A task belongs to one user (user_id references User.id)

### Session
Represents an active authenticated user session with security token validity.

**Fields**:
- id (UUID/String): Unique identifier for the session (Primary Key)
- user_id (UUID/String): Foreign key linking to the user (Required)
- token (String): JWT token identifier (Required, Unique)
- expires_at (DateTime): Expiration timestamp for the session (Required)
- created_at (DateTime): Timestamp when session was created (Required, Auto-generated)
- is_active (Boolean): Whether the session is still valid (Default: True)

**Validation Rules**:
- User_id must reference an existing user
- Token must be unique across all sessions
- Expires_at must be in the future
- Session becomes inactive after expiration

**Relationships**:
- Many-to-One: A session belongs to one user (user_id references User.id)

## Indexes

### Required Indexes
- User.email: For efficient user lookup by email during authentication
- Task.user_id: For efficient querying of tasks by user
- Task.completed: For efficient filtering of completed vs incomplete tasks
- Session.token: For efficient session validation by token
- Session.expires_at: For efficient cleanup of expired sessions

## State Transitions

### Task State Transitions
- Incomplete → Complete: When user marks task as complete
- Complete → Incomplete: When user unmarks task as complete

### Session State Transitions
- Active → Inactive: When session expires or user logs out

## Business Rules

1. **Ownership Rule**: Users can only access and modify their own tasks
2. **Creation Rule**: Users can only create tasks for themselves
3. **Deletion Rule**: Users can only delete their own tasks
4. **Authentication Rule**: All operations require valid authentication token
5. **Privacy Rule**: Task data must be isolated between users at the database level
6. **Persistence Rule**: All tasks must be persisted in the database
7. **Timestamp Rule**: Creation and update timestamps must be automatically managed

## Constraints

1. **Referential Integrity**: Foreign keys must reference existing records
2. **Data Validation**: All inputs must be validated before database insertion
3. **Security Constraint**: User ID must be verified from JWT token, not from request payload
4. **Access Control**: Database queries must filter by authenticated user ID