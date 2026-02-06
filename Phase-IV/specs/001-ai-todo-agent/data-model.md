# Data Model: AI Todo Agent

## Entity Definitions

### Task
**Description**: Represents a user's task that can be managed through the AI assistant

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

### Conversation
**Description**: Represents a conversation thread between user and AI assistant

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `user_id`: String (Foreign Key to User, Required)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-generated, Updates on change)

**Constraints**:
- user_id must match authenticated user
- Index on user_id for efficient querying

**Validations**:
- user_id format validation

### Message
**Description**: Represents individual messages within a conversation

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `user_id`: String (Foreign Key to User, Required)
- `conversation_id`: Integer (Foreign Key to Conversation, Required)
- `role`: String (Required, Values: "user" | "assistant")
- `content`: String (Required, Max length: 5000)
- `created_at`: DateTime (Auto-generated)

**Constraints**:
- user_id must match authenticated user
- conversation_id must exist
- role must be either "user" or "assistant"
- Index on (conversation_id, created_at) for chronological ordering

**Validations**:
- user_id format validation
- content length between 1-5000 characters
- role value validation

## Relationships

### Task Relationships
- **Belongs to**: User (via user_id foreign key)
- **Access control**: Only user with matching user_id can access tasks

### Conversation Relationships
- **Belongs to**: User (via user_id foreign key)
- **Has many**: Messages (via conversation_id foreign key)
- **Access control**: Only user with matching user_id can access conversations

### Message Relationships
- **Belongs to**: User (via user_id foreign key)
- **Belongs to**: Conversation (via conversation_id foreign key)
- **Access control**: Only user with matching user_id can access messages

## State Transitions

### Task State Transitions
- **Creation**: New task created with `completed = false`
- **Completion**: `completed` changes from `false` to `true`
- **Reopening**: `completed` changes from `true` to `false` (if feature supported)
- **Deletion**: Task marked as deleted (soft delete) or removed entirely

### Message State Transitions
- **Creation**: New message added to conversation with `role` set to "user" or "assistant"
- **No further transitions**: Messages are immutable after creation

## Indexing Strategy

### Primary Indexes
- Task.id (Primary Key)
- Conversation.id (Primary Key)
- Message.id (Primary Key)

### Secondary Indexes
- Task.user_id (For user-specific queries)
- Task.user_id, Task.completed (For user's pending/completed tasks)
- Conversation.user_id (For user's conversations)
- Message.conversation_id, Message.created_at (For chronological message retrieval)
- Message.user_id (For user-specific message queries)

## Validation Rules

### Business Logic Validations
1. **User Isolation**: All queries must filter by user_id to prevent cross-user access
2. **Task Ownership**: Users can only modify tasks they own
3. **Conversation Ownership**: Users can only access their own conversations and messages
4. **Data Integrity**: Foreign key constraints ensure referential integrity

### Input Validations
1. **Task Title**: Required, 1-255 characters
2. **Task Description**: Optional, 0-1000 characters
3. **Message Content**: Required, 1-5000 characters
4. **Role Values**: Must be either "user" or "assistant"