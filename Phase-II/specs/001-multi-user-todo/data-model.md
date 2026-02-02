# Data Model: Multi-user Todo Web Application

## Overview
Data model for the secure, multi-user todo web application with authentication and data isolation.

## Entities

### User
Represents an authenticated user account managed by Better Auth
- **id**: string/uuid (Primary Key) - Unique identifier for the user
- **email**: string (Unique) - User's email address for authentication
- **created_at**: timestamptz - Timestamp when the user account was created

*Note: User entity is primarily managed by Better Auth system*

### Task
Represents a todo item with title, description, completion status, and user ownership
- **id**: serial/uuid (Primary Key) - Unique identifier for the task
- **user_id**: string/uuid (Foreign Key → users.id, Indexed) - Reference to the owning user
- **title**: varchar(200) (NOT NULL) - Title of the task
- **description**: text (NULL) - Optional detailed description of the task
- **completed**: boolean (DEFAULT false) - Whether the task is completed
- **created_at**: timestamptz (DEFAULT now()) - Timestamp when the task was created
- **updated_at**: timestamptz (DEFAULT now()) - Timestamp when the task was last updated

## Relationships
- **Task** belongs to **User** (Many-to-One relationship)
  - Task.user_id → User.id
  - Foreign key constraint ensures referential integrity
  - Index on user_id for efficient querying of user's tasks

## Constraints
- All tasks must have a valid user_id (foreign key constraint)
- Users can only access tasks where user_id matches their authenticated user_id
- Task titles are limited to 200 characters for consistency
- Automatic timestamp management for created_at and updated_at fields

## Access Patterns
- Query tasks by user_id (authenticated user's tasks)
- Filter tasks by completion status
- Search tasks by title or description
- Create new tasks for authenticated user
- Update/delete tasks owned by authenticated user