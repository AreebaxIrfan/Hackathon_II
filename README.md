# Full-Stack Todo Web Application

A secure, multi-user todo application with authentication, persistent storage, and RESTful API.

## Features

- User registration and authentication with JWT
- Secure task management (Create, Read, Update, Delete, Complete)
- Multi-user data isolation
- Persistent storage with PostgreSQL
- Responsive web interface

## Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript
- **Backend**: Python FastAPI
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Authentication**: Better Auth (JWT-based)

## Setup Instructions

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database URL and secrets
   ```

4. Initialize the database:
   ```bash
   python -m src.database.init_db
   ```

   Or using Alembic:
   ```bash
   cd backend
   alembic upgrade head
   ```

5. Start the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.local.example .env.local
   # Edit .env.local with your API base URL and secrets
   ```

4. Start the frontend development server:
   ```bash
   npm run dev
   ```

## API Endpoints

The API is available at `http://localhost:8000/api`.

### Authentication Endpoints

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login with existing credentials
- `POST /api/auth/logout` - Logout current user
- `GET /api/auth/profile` - Get current user profile

### Task Management Endpoints

- `GET /api/tasks` - Get current user's tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get specific task by ID
- `PUT /api/tasks/{id}` - Update specific task
- `DELETE /api/tasks/{id}` - Delete specific task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing
- `DEBUG`: Enable/disable debug mode (true/false)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL
- `NEXTAUTH_SECRET`: Secret key matching backend
- `NEXTAUTH_URL`: Frontend application URL

## Database Migrations

This application uses Alembic for database migrations:

1. To create a new migration:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Description of changes"
   ```

2. To apply migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```

## Security Features

- JWT-based authentication with secure token handling
- User data isolation - users can only access their own tasks
- Input validation and sanitization
- Password hashing using bcrypt
- SQL injection prevention through ORM usage

## Development

### Running Tests

Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
cd frontend
npm run test
```

### Project Structure

```
backend/
├── src/
│   ├── models/      # Database models
│   ├── services/    # Business logic
│   ├── api/         # API endpoints
│   ├── database/    # Database connection and setup
│   ├── utils/       # Utility functions
│   └── core/        # Configuration and core components
├── alembic/         # Database migrations
└── requirements.txt

frontend/
├── src/
│   ├── components/  # React components
│   ├── pages/       # Page components
│   ├── lib/         # Utilities and API client
│   ├── services/    # Business logic
│   ├── types/       # TypeScript type definitions
│   └── context/     # React context providers
├── public/
└── package.json
```

## Deployment

1. Build the frontend:
   ```bash
   cd frontend
   npm run build
   ```

2. Ensure environment variables are properly set for production
3. Run the backend with a production ASGI server like gunicorn:
   ```bash
   gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```