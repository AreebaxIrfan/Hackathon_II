# Data Model: Chat Flow & API for Stateless Todo Assistant

## Entity Definitions

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

### ToolCall
**Description**: Represents an invocation of an MCP tool during conversation processing

**Fields**:
- `id`: Integer (Primary Key, Auto-generated)
- `conversation_id`: Integer (Foreign Key to Conversation, Required)
- `tool_name`: String (Required, Max length: 100)
- `arguments`: JSON (Required, Max length: 5000)
- `result`: JSON (Optional, Max length: 5000)
- `created_at`: DateTime (Auto-generated)

**Constraints**:
- conversation_id must exist
- tool_name must be a valid MCP tool
- Index on conversation_id for efficient querying

**Validations**:
- tool_name validation against registered tools
- arguments and result JSON format validation

## Relationships

### Conversation Relationships
- **Belongs to**: User (via user_id foreign key)
- **Has many**: Messages (via conversation_id foreign key)
- **Has many**: ToolCalls (via conversation_id foreign key)
- **Access control**: Only user with matching user_id can access conversations

### Message Relationships
- **Belongs to**: User (via user_id foreign key)
- **Belongs to**: Conversation (via conversation_id foreign key)
- **Access control**: Only user with matching user_id can access messages

### ToolCall Relationships
- **Belongs to**: Conversation (via conversation_id foreign key)
- **Access control**: Only accessible through the conversation's user

## State Transitions

### Message State Transitions
- **Creation**: New message added to conversation with `role` set to "user" or "assistant"
- **No further transitions**: Messages are immutable after creation

### ToolCall State Transitions
- **Creation**: New tool call recorded with arguments
- **Completion**: Result added after tool execution (if applicable)
- **Error**: Error details added if tool execution fails

## Indexing Strategy

### Primary Indexes
- Conversation.id (Primary Key)
- Message.id (Primary Key)
- ToolCall.id (Primary Key)

### Secondary Indexes
- Conversation.user_id (For user-specific queries)
- Message.conversation_id, Message.created_at (For chronological message retrieval)
- Message.user_id (For user-specific message queries)
- ToolCall.conversation_id (For conversation-specific tool calls)

## Validation Rules

### Business Logic Validations
1. **User Isolation**: All queries must filter by user_id to prevent cross-user access
2. **Conversation Ownership**: Users can only access conversations they own
3. **Message Ownership**: Users can only access messages in conversations they own
4. **Data Integrity**: Foreign key constraints ensure referential integrity

### Input Validations
1. **Message Content**: Required, 1-5000 characters
2. **Message Role**: Must be either "user" or "assistant"
3. **Tool Name**: Must be a valid registered MCP tool
4. **Arguments/Result**: Must be valid JSON format