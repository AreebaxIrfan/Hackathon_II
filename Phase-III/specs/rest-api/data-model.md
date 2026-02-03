# Data Model for Task Management API

## Entities

### Task
- **id**: UUID (Primary Key)
- **title**: String (Required, 1-255 characters)
- **description**: String (Optional, max 1000 characters)
- **completed**: Boolean (Default: false)
- **priority**: Integer (Range: 1-5, Default: 1)
- **user_id**: UUID (Foreign Key to User, Required)
- **created_at**: DateTime (Auto-generated)
- **updated_at**: DateTime (Auto-generated)

## Relationships
- Task belongs to User (Many-to-One)
- User has many Tasks (One-to-Many)

## Validation Rules
- Title must be 1-255 characters
- Description can be null, max 1000 characters
- Priority must be between 1 and 5
- Completed defaults to false
- user_id is required and must reference an existing user

## State Transitions
- Task can transition from pending (completed: false) to completed (completed: true)
- Task can transition from completed (completed: true) to pending (completed: false)