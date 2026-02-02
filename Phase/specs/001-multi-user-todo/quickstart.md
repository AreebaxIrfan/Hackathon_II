# Quickstart Guide: Multi-user Todo Web Application

## Overview
Quick start guide for setting up and running the secure, multi-user todo web application.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- PostgreSQL-compatible database (Neon Serverless recommended)
- Git for version control

## Environment Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and auth secrets
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your backend API URL and auth configuration
```

## Configuration

### Backend Configuration
1. **Database**: Set `DATABASE_URL` in `.env` to your Neon PostgreSQL connection string
2. **Authentication**: Set `BETTER_AUTH_SECRET` in `.env` for JWT signing
3. **Environment**: Adjust other settings in `.env` as needed

### Frontend Configuration
1. **API URL**: Set `NEXT_PUBLIC_API_URL` in `.env.local` to your backend URL
2. **Auth Settings**: Configure `NEXT_PUBLIC_BETTER_AUTH_URL` for Better Auth integration

## Running the Application

### Development Mode
```bash
# Terminal 1: Start backend
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py

# Terminal 2: Start frontend
cd frontend
npm run dev
# or
yarn dev
```

### Database Initialization
```bash
# In backend directory
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -c "from src.db.init import init_db; init_db()"
```

## Key Features

### User Authentication
- Visit `/auth/register` to create an account
- Visit `/auth/login` to sign in
- Protected routes automatically redirect unauthenticated users

### Task Management
- Visit `/dashboard` or `/todos` to view your tasks
- Create new tasks using the form
- Toggle task completion status with checkboxes
- Edit or delete your tasks

## API Endpoints
- **Frontend**: Available at `http://localhost:3000`
- **Backend API**: Available at `http://localhost:8000/api`
- **Documentation**: Auto-generated with Swagger at `http://localhost:8000/docs`

## Testing
```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test
# or
yarn test
```

## Deployment Notes
- For Neon PostgreSQL, use connection pooling settings appropriate for your plan
- Ensure CORS settings allow your frontend domain in production
- Set secure, production-grade values for auth secrets
- Consider using a reverse proxy in production deployments