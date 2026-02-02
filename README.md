# Full-Stack Todo Web Application

This project implements a secure multi-user todo application with authentication, JWT-based API access, and persistent storage. Users can sign up, log in, manage tasks, and access protected resources.

## Features

- User registration and authentication with JWT
- Secure task management (Create, Read, Update, Delete, Complete)
- Multi-user data isolation
- Persistent storage with PostgreSQL
- Responsive web interface

## Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript
- **Backend**: Python FastAPI
- **Database**: PostgreSQL / Neon Serverless
- **ORM**: SQLModel
- **Authentication**: JWT tokens, bcrypt password hashing
- **Security**: Environment-based secret management

## Setup Instructions

### Backend

1. `cd backend`
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and edit secrets
4. Initialize DB: `python -m src.database.init_db` or `alembic upgrade head`
5. Start server: `uvicorn src.main:app --reload --port 8000`

### Frontend

1. `cd frontend`
2. `npm install`
3. `cp .env.local.example .env.local` and set API URL
4. `npm run dev`

## API Endpoints

### Authentication

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/profile`

### Tasks

- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/tasks/{id}`
- `PUT /api/tasks/{id}`
- `DELETE /api/tasks/{id}`
- `PATCH /api/tasks/{id}/complete`
