# Quickstart Guide: Full-Stack Todo Web Application

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Git for version control
- Docker (optional, for containerized development)

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup (Python/FastAPI)

#### Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Environment Configuration
Create a `.env` file in the backend directory with the following variables:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
```

#### Database Initialization
```bash
# Run database migrations
python -m alembic upgrade head
```

#### Start Backend Server
```bash
# Development mode
uvicorn src.main:app --reload --port 8000

# Production mode
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup (Next.js)

#### Install Frontend Dependencies
```bash
cd frontend
npm install
```

#### Environment Configuration
Create a `.env.local` file in the frontend directory with the following variables:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXTAUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
NEXTAUTH_URL=http://localhost:3000
```

#### Start Frontend Development Server
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 4. Better Auth Configuration

The frontend is configured with Better Auth for user registration and authentication. Ensure the following:

1. The `BETTER_AUTH_SECRET` matches between frontend and backend
2. The authentication endpoints are properly configured
3. JWT tokens are correctly handled between frontend and backend

## API Endpoints

### Authentication Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login existing user
- `POST /api/auth/logout` - Logout current user

### Task Management Endpoints
- `GET /api/tasks` - Get current user's tasks
- `POST /api/tasks` - Create new task for current user
- `GET /api/tasks/{id}` - Get specific task by ID
- `PUT /api/tasks/{id}` - Update specific task
- `DELETE /api/tasks/{id}` - Delete specific task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Development Workflow

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

### Building for Production
```bash
# Build frontend for production
cd frontend
npm run build

# Backend is ready to deploy as-is with proper configuration
```

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret key for JWT token signing
- `DEBUG`: Enable/disable debug mode (true/false)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL
- `NEXTAUTH_SECRET`: Secret key matching backend
- `NEXTAUTH_URL`: Frontend application URL

## Database Schema

The application uses SQLModel to define database models. Key tables include:

- `users`: Stores user account information
- `tasks`: Stores individual tasks linked to users
- `sessions`: Tracks active user sessions (if applicable)

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify DATABASE_URL is correct
   - Ensure PostgreSQL server is running
   - Check firewall settings

2. **Authentication Issues**:
   - Verify that BETTER_AUTH_SECRET matches between frontend and backend
   - Check that JWT tokens are being properly passed in headers

3. **CORS Issues**:
   - Ensure frontend URL is allowed in backend CORS configuration
   - Check that API requests include proper authentication headers

### Useful Commands

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend build
cd frontend && npm run build && npm run start
```

## Deployment

For production deployment:

1. Set up PostgreSQL database (Neon Serverless recommended)
2. Configure environment variables for production
3. Build frontend assets
4. Deploy backend with proper process management (PM2, systemd, etc.)
5. Configure reverse proxy (nginx, Apache) if needed
6. Set up SSL certificates for HTTPS