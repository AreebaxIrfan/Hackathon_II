# Quickstart Guide for Full-Stack Web Application

## Development Setup

### Prerequisites
- Node.js 18+ installed
- Python 3.9+ installed
- PostgreSQL-compatible database (Neon recommended)
- Git installed

### Environment Configuration
1. Copy `.env.example` to `.env` in both frontend and backend directories
2. Set up Neon PostgreSQL database and update connection string
3. Configure Better Auth environment variables
4. Set JWT secret for token signing

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Run database migrations
alembic upgrade head
# Start the development server
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
# Start the development server
npm run dev
```

## API Testing

### Authentication Flow
1. Register a new user:
   ```
   POST /auth/register
   Content-Type: application/json
   {
     "email": "test@example.com",
     "password": "securePassword123"
   }
   ```

2. Login to get JWT token:
   ```
   POST /auth/login
   Content-Type: application/json
   {
     "email": "test@example.com",
     "password": "securePassword123"
   }
   ```

3. Use JWT token for authenticated requests:
   ```
   GET /tasks
   Authorization: Bearer <token>
   ```

### Task Management Flow
1. Create a task:
   ```
   POST /tasks
   Authorization: Bearer <token>
   Content-Type: application/json
   {
     "title": "Sample task",
     "description": "This is a sample task description"
   }
   ```

2. Get user's tasks:
   ```
   GET /tasks
   Authorization: Bearer <token>
   ```

3. Update a task:
   ```
   PUT /tasks/<task-id>
   Authorization: Bearer <token>
   Content-Type: application/json
   {
     "title": "Updated task title",
     "description": "Updated description"
   }
   ```

4. Mark task as complete:
   ```
   PATCH /tasks/<task-id>/complete
   Authorization: Bearer <token>
   ```

## Frontend Development

### Key Components
- `components/auth/` - Authentication UI components
- `components/tasks/` - Task management UI components
- `lib/auth.js` - Authentication utilities
- `lib/api.js` - API client with JWT handling

### Running Tests
```bash
# Frontend tests
npm run test

# Backend tests
pytest
```

## Common Issues

### Database Connection
- Ensure Neon PostgreSQL connection string is correctly formatted
- Check that SSL mode is properly configured
- Verify database credentials and permissions

### Authentication
- Confirm Better Auth is properly configured
- Check JWT secret is consistent between frontend and backend
- Verify CORS settings allow frontend-backend communication

### Deployment
- Ensure environment variables are set in production
- Run database migrations in production environment
- Configure SSL certificates for HTTPS

## Next Steps

1. Complete the user authentication flow
2. Implement task management features
3. Add advanced filtering and search capabilities
4. Implement user preferences and settings
5. Add error handling and validation