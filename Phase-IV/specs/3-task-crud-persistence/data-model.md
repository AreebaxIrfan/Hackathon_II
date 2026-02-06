# Data Model for Task CRUD & Data Persistence

## Task Entity

### Fields
- `id`: UUID (Primary Key, auto-generated)
- `user_id`: UUID (Foreign Key to users.id, Indexed, Required)
- `title`: String (Required, Max 255 chars)
- `description`: Text (Optional, Max 1000 chars)
- `completed`: Boolean (Default: false, Indexed)
- `priority`: Integer (Optional, Default: 1, Range: 1-5)
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
- Priority: Optional integer between 1-5, default 1

## User Entity (Referenced)

### Fields
- `id`: UUID (Primary Key, auto-generated)
- `email`: String (Unique, Indexed, Required)
- `hashed_password`: String (Required)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated)
- `is_active`: Boolean (Default: true)

### Relationships
- One-to-Many: User → Tasks (user.tasks)

## Database Schema Design

### Tables
```
tasks
├── id (UUID, PK)
├── user_id (UUID, FK → users.id)
├── title (VARCHAR)
├── description (TEXT)
├── completed (BOOLEAN)
├── priority (INTEGER)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

users
├── id (UUID, PK)
├── email (VARCHAR, UNIQUE)
├── hashed_password (VARCHAR)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── is_active (BOOLEAN)
```

### Indexes
- `tasks.user_id`: For efficient user-scoped queries
- `tasks.completed`: For filtering by completion status
- `tasks.created_at`: For chronological ordering
- `tasks.priority`: For priority-based sorting
- `users.email`: For efficient login lookups

### Constraints
- Foreign Key: tasks.user_id → users.id (NO ACTION on update, CASCADE on delete)
- Not Null: All required fields
- Check: Priority values between 1-5 (if supported by database)
- Unique: Users email constraint

## State Transitions

### Task Completion
- `completed: false` → `completed: true` (via complete endpoint)
- `completed: true` → `completed: false` (via incomplete endpoint)

## Query Patterns

### Common Queries
1. Get user's tasks: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`
2. Get pending tasks: `SELECT * FROM tasks WHERE user_id = ? AND completed = false ORDER BY priority DESC, created_at ASC`
3. Get completed tasks: `SELECT * FROM tasks WHERE user_id = ? AND completed = true ORDER BY updated_at DESC`
4. Get specific task: `SELECT * FROM tasks WHERE id = ? AND user_id = ?`
5. Count user's tasks: `SELECT COUNT(*) FROM tasks WHERE user_id = ?`

### Performance Considerations
- Composite indexes for multi-field queries (user_id + completed)
- Proper indexing for authenticated user scoping
- Efficient pagination for large task lists
- Priority-based sorting with index optimization