# Data Model: MCP Tools for Todo Management

## Entity Definitions

### Task
**Description**: Represents a user's task that can be managed through the MCP tools

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `user_id`: String (Foreign Key to User, Required)
- `title`: String (Required, Max length: 255)
- `description`: String (Optional, Max length: 1000)
- `completed`: Boolean (Default: false)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, Updates on change)

**Constraints**:
- Title must not be empty
- user_id must match authenticated user
- Index on (user_id, completed) for efficient querying

**Validations**:
- Title length between 1-255 characters
- Description length up to 1000 characters
- user_id format validation

## Relationships

### Task Relationships
- **Belongs to**: User (via user_id foreign key)
- **Access control**: Only user with matching user_id can access tasks

## State Transitions

### Task State Transitions
- **Creation**: New task created with `completed = false`
- **Completion**: `completed` changes from `false` to `true`
- **Reopening**: `completed` changes from `true` to `false` (if feature supported)
- **Deletion**: Task marked as deleted (soft delete) or removed entirely

## Indexing Strategy

### Primary Indexes
- Task.id (Primary Key)

### Secondary Indexes
- Task.user_id (For user-specific queries)
- Task.user_id, Task.completed (For user's pending/completed tasks)

## Validation Rules

### Business Logic Validations
1. **User Isolation**: All queries must filter by user_id to prevent cross-user access
2. **Task Ownership**: Users can only modify tasks they own
3. **Data Integrity**: Foreign key constraints ensure referential integrity

### Input Validations
1. **Task Title**: Required, 1-255 characters
2. **Task Description**: Optional, 0-1000 characters