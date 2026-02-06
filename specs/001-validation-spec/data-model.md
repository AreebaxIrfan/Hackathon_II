# Data Model: Frontend & Backend Validation

**Feature**: 001-validation-spec
**Date**: 2026-02-05

## Entities

### User
- **Description**: Represents an authenticated user of the Todo application
- **Fields**:
  - id: UUID (Primary Key)
  - email: String (Unique, Indexed)
  - username: String (Unique, Optional)
  - hashed_password: String (Securely hashed)
  - created_at: DateTime (Default: now)
  - updated_at: DateTime (Default: now, Auto-update)
  - is_active: Boolean (Default: True)
- **Relationships**:
  - One-to-Many: User → Todos
  - One-to-Many: User → Conversations
- **Validation**:
  - Email format validation
  - Password strength requirements
  - Unique constraint on email

### Todo
- **Description**: Represents a user's task/todo item
- **Fields**:
  - id: UUID (Primary Key)
  - title: String (Required, Max length: 200)
  - description: Text (Optional)
  - completed: Boolean (Default: False)
  - user_id: UUID (Foreign Key to User.id, Required)
  - created_at: DateTime (Default: now)
  - updated_at: DateTime (Default: now, Auto-update)
  - due_date: DateTime (Optional)
- **Relationships**:
  - Many-to-One: Todo ← User
- **Validation**:
  - Title must not be empty
  - User_id must reference existing user
  - Completed status is boolean

### Conversation
- **Description**: Represents a chat conversation session
- **Fields**:
  - id: UUID (Primary Key)
  - user_id: UUID (Foreign Key to User.id, Required)
  - title: String (Generated from first message or topic)
  - created_at: DateTime (Default: now)
  - updated_at: DateTime (Default: now, Auto-update)
- **Relationships**:
  - Many-to-One: Conversation ← User
  - One-to-Many: Conversation → ChatMessages
- **Validation**:
  - User_id must reference existing user

### ChatMessage
- **Description**: Represents an individual message in a chat conversation
- **Fields**:
  - id: UUID (Primary Key)
  - conversation_id: UUID (Foreign Key to Conversation.id, Required)
  - sender_type: String (Enum: 'user', 'assistant', Required)
  - content: Text (Required)
  - timestamp: DateTime (Default: now)
  - metadata: JSON (Optional, for additional context)
- **Relationships**:
  - Many-to-One: ChatMessage ← Conversation
- **Validation**:
  - Conversation_id must reference existing conversation
  - Sender_type must be one of allowed values
  - Content must not be empty

## Relationships

### User ↔ Todo (One-to-Many)
- One user can have many todos
- Each todo belongs to exactly one user
- Cascade delete: When user is deleted, all their todos are deleted
- Foreign key constraint on user_id in Todo table

### User ↔ Conversation (One-to-Many)
- One user can have many conversations
- Each conversation belongs to exactly one user
- Cascade delete: When user is deleted, all their conversations are deleted
- Foreign key constraint on user_id in Conversation table

### Conversation ↔ ChatMessage (One-to-Many)
- One conversation can have many messages
- Each message belongs to exactly one conversation
- Cascade delete: When conversation is deleted, all its messages are deleted
- Foreign key constraint on conversation_id in ChatMessage table

## Business Rules

1. **Data Isolation**: Users can only access their own todos and conversations
2. **Authorization**: All operations require valid user authentication
3. **Soft Deletes**: Consider implementing soft deletes for audit trail (optional)
4. **Unique Constraints**: Email uniqueness at database level
5. **Indexing**: Primary access patterns should be indexed (user_id, timestamps)

## Validation Rules

1. **User Validation**:
   - Email format compliance
   - Password complexity (min 8 chars, mixed case, numbers)
   - Username uniqueness (if provided)

2. **Todo Validation**:
   - Title required and not empty
   - Title length maximum 200 characters
   - Date formats must be valid

3. **Message Validation**:
   - Content must not be empty or whitespace only
   - Sender type restricted to allowed values
   - Timestamp automatically set

## State Transitions

### Todo State Transitions
- Created → Active (default)
- Active ↔ Completed (via update operation)
- Any state → Deleted (via delete operation)

### User State Transitions
- Registered → Active (default)
- Active ↔ Inactive (admin action)
- Active/Inactive → Deleted (user or admin action)

## Access Patterns

1. **Frequent Queries**:
   - Get all todos for a specific user
   - Get all conversations for a specific user
   - Get messages for a specific conversation

2. **Indexing Strategy**:
   - User.id for user lookups
   - Todo.user_id for todo filtering
   - Conversation.user_id for conversation filtering
   - ChatMessage.conversation_id for message retrieval
   - Todo.created_at for chronological sorting