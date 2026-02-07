# Research Document: Phase IV - Local Kubernetes Deployment

## Overview
This document consolidates research findings about the existing Todo Chatbot application (Phase III) to inform the Kubernetes deployment strategy.

## Application Architecture
The existing application consists of two main components:

### Backend (Python/FastAPI)
- **Location**: `./backend/`
- **Framework**: FastAPI with Python 3.9+
- **Main entry point**: `./backend/main.py`
- **Key dependencies**: FastAPI, SQLModel, Uvicorn, OpenAI, asyncpg, Alembic
- **Startup command**: `uvicorn src.main:app --reload`
- **Port**: Runs on standard FastAPI port (defaults to 8000)
- **Database**: Neon PostgreSQL (via asyncpg)
- **Health check endpoint**: `/health`
- **Primary API endpoint**: `/api/{user_id}/chat` for the AI chat functionality

### Frontend (Next.js/React)
- **Location**: `./frontend/`
- **Framework**: Next.js 16+, React 19+
- **Key dependencies**: Next.js, React, @openai/chat-components
- **Startup command**: `npm run dev` (development) or `npm start` (production)
- **Port**: Runs on port 3000
- **Key functionality**: Chat interface using OpenAI ChatKit connected to backend API

## Deployment Considerations

### Containerization Requirements
- **Backend**: Need Python base image with dependencies installed from requirements.txt
- **Frontend**: Need Node.js base image with Next.js application built
- **Ports**: Backend (likely 8000), Frontend (likely 3000)
- **Environment variables**: Both components likely need ENV vars for configuration

### Kubernetes Deployment Strategy
- **Two services**: Separate deployments for frontend and backend
- **Database**: Need Neon PostgreSQL connection (may require external access or migration)
- **Service communication**: Frontend needs to connect to backend API
- **Ingress/load balancing**: Access to both frontend and backend services

### AI Tools Integration (for AI-assisted deployment)
- **Gordon**: For Dockerfile generation and optimization
- **kubectl-ai**: For Kubernetes deployment management
- **Kagent**: For cluster operations and monitoring

## Technical Decisions

### Decision: Containerization Approach
**Chosen**: Multi-container approach with separate Dockerfiles for frontend and backend
**Rationale**: Maintains separation of concerns, allows independent scaling and updates, follows microservices principles
**Alternatives considered**:
- Single container with both frontend and backend (rejected - tight coupling)
- Server-side rendering approach (rejected - complexity, different architecture)

### Decision: Database Connection Strategy
**Chosen**: Maintain connection to existing Neon PostgreSQL database
**Rationale**: Avoids data migration complexity and maintains continuity of existing data
**Alternatives considered**:
- Kubernetes PostgreSQL deployment (rejected - data migration required, complexity)
- SQLite volume persistence (rejected - not suitable for production, performance)

### Decision: Service Communication Pattern
**Chosen**: Standard service-to-service communication via Kubernetes services
**Rationale**: Follows Kubernetes best practices, enables proper load balancing and discovery
**Alternatives considered**:
- Direct IP addressing (rejected - not resilient to pod restarts)
- External load balancer for each service (rejected - unnecessary complexity)

### Decision: Ingress Strategy
**Chosen**: Kubernetes Ingress controller for external access
**Rationale**: Provides unified access point, enables SSL termination, handles routing rules
**Alternatives considered**:
- LoadBalancer services (rejected - costs and complexity)
- NodePort services (rejected - limited ports, security concerns)

## Kubernetes Resource Requirements

### Backend Deployment
- CPU: 500m (minimum), 1000m (recommended)
- Memory: 512Mi (minimum), 1Gi (recommended)
- Storage: None required (ephemeral storage)
- Environment variables: Database connection, API keys

### Frontend Deployment
- CPU: 200m (minimum), 500m (recommended)
- Memory: 256Mi (minimum), 512Mi (recommended)
- Storage: None required (ephemeral storage)
- Environment variables: Backend API URL

## Helm Chart Structure
The Helm chart will include:
- Chart.yaml with metadata
- values.yaml with configurable parameters
- templates/ directory with:
  - backend deployment and service
  - frontend deployment and service
  - ingress configuration
  - configmaps/secrets for environment variables

## Best Practices Applied
- Proper resource limits and requests for both services
- Health checks for liveness and readiness probes
- Proper service accounts and RBAC if needed
- Security context configurations
- Pod disruption budgets for high availability