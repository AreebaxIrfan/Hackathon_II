# Data Model for Full-Stack Web Application

## User Entity

### Fields
- `id`: UUID (Primary Key, auto-generated)
- `email`: String (Unique, Indexed, Required)
- `hashed_password`: String (Required, Min 60 chars for bcrypt hash)
- `created_at`: DateTime (Auto-generated, Indexed)
- `updated_at`: DateTime (Auto-generated, updates on change)
- `is_active`: Boolean (Default: true)

### Relationships
- One-to-Many: User → Tasks (user.tasks)

### Validation Rules
- Email: Must be valid email format
- Password: Hashed using bcrypt (strength configurable)
- Email uniqueness: Enforced at database level
- Active status: Controls login capability

## Task Entity

### Fields
- `id`: UUID (Primary Key, auto-generated)
- `user_id`: UUID (Foreign Key to users.id, Indexed, Required)
- `title`: String (Required, Max 255 chars)
- `description`: Text (Optional, Max 1000 chars)
- `completed`: Boolean (Default: false, Indexed)
- `created_at`: DateTime (Auto-generated, Indexed)
- `updated_at`: DateTime (Auto-generated, updates on change)

### Relationships
- Many-to-One: Task → User (task.user)
- Indexes: user_id and completed for efficient querying

### Validation Rules
- Title: Required, 1-255 characters
- Description: Optional, 0-1000 characters
- User association: Required, must reference existing user
- Completion status: Boolean value only

## Database Schema Design

### Tables
```
users
├── id (UUID, PK)
├── email (VARCHAR, UNIQUE)
├── hashed_password (VARCHAR)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── is_active (BOOLEAN)

tasks
├── id (UUID, PK)
├── user_id (UUID, FK → users.id)
├── title (VARCHAR)
├── description (TEXT)
├── completed (BOOLEAN)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

### Indexes
- `users.email`: For efficient login lookups
- `users.created_at`: For user activity queries
- `tasks.user_id`: For user-scoped queries
- `tasks.completed`: For filtering by completion status
- `tasks.created_at`: For chronological ordering

### Constraints
- Foreign Key: tasks.user_id → users.id (CASCADE DELETE)
- Unique: users.email
- Not Null: All required fields
- Check: email format validation (if supported by database)

## State Transitions

### Task Completion
- `completed: false` → `completed: true` (via complete endpoint)
- `completed: true` → `completed: false` (via incomplete endpoint)

### User Activation
- `is_active: true` → `is_active: false` (account deactivation)
- `is_active: false` → `is_active: true` (account reactivation)

## Query Patterns

### Common Queries
1. Get user's tasks: `SELECT * FROM tasks WHERE user_id = ?`
2. Get pending tasks: `SELECT * FROM tasks WHERE user_id = ? AND completed = false`
3. Get completed tasks: `SELECT * FROM tasks WHERE user_id = ? AND completed = true`
4. Check user existence: `SELECT id FROM users WHERE email = ? AND is_active = true`

### Performance Considerations
- Composite indexes for multi-field queries
- Proper indexing for authenticated user scoping
- Efficient pagination for large task lists