# Data Model for Database Schema & Persistence

## Entities

### User
- **id**: UUID (Primary Key, Auto-generated)
- **email**: String (Unique, Required, Indexed)
- **hashed_password**: String (Required)
- **first_name**: String (Optional)
- **last_name**: String (Optional)
- **is_active**: Boolean (Default: true)
- **created_at**: DateTime (Auto-generated)
- **updated_at**: DateTime (Auto-generated, Updates on change)

### Task
- **id**: UUID (Primary Key, Auto-generated)
- **title**: String (Required, 1-255 characters)
- **description**: String (Optional, max 1000 characters)
- **completed**: Boolean (Default: false)
- **priority**: Integer (Range: 1-5, Default: 1)
- **user_id**: UUID (Foreign Key to User, Required, Indexed)
- **created_at**: DateTime (Auto-generated)
- **updated_at**: DateTime (Auto-generated, Updates on change)

## Relationships
- Task belongs to User (Many-to-One)
- User has many Tasks (One-to-Many)
- Foreign Key Constraint: task.user_id → user.id
- Cascade Delete: When user is deleted, all associated tasks are deleted

## Validation Rules
- User email must be valid email format
- User email must be unique across all users
- Task title must be 1-255 characters
- Task description can be null, max 1000 characters
- Task priority must be between 1 and 5
- Task completed defaults to false
- User_id is required and must reference an existing user

## Indexes
- User.email: Unique index for fast user lookup
- Task.user_id: Index for efficient user-scoped queries
- Task.created_at: Index for chronological ordering
- Task.completed: Index for filtering by completion status
- Composite index: (user_id, created_at) for efficient user task retrieval with ordering

## State Transitions
- Task can transition from pending (completed: false) to completed (completed: true)
- Task can transition from completed (completed: true) to pending (completed: false)
- User can transition from active (is_active: true) to inactive (is_active: false)