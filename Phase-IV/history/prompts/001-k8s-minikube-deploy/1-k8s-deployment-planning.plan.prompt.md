---
id: 1
title: K8s Deployment Planning
stage: plan
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-k8s-minikube-deploy
branch: 001-k8s-minikube-deploy
user: Claude User
command: sp.plan
labels: [kubernetes, minikube, deployment, ai-devops, helm, docker]
links:
  spec: D:/phase-three/specs/001-k8s-minikube-deploy/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - D:/phase-three/specs/001-k8s-minikube-deploy/plan.md
  - D:/phase-three/specs/001-k8s-minikube-deploy/research.md
  - D:/phase-three/specs/001-k8s-minikube-deploy/data-model.md
  - D:/phase-three/specs/001-k8s-minikube-deploy/quickstart.md
  - D:/phase-three/specs/001-k8s-minikube-deploy/contracts/deployment-api.yaml
tests:
  - none
---

## Prompt

# SP-01 Plan: System Overview

- Review Phase Todo Chatbot scope
- Identify Phase IV deployment goals
- Confirm local-only Kubernetes environment
- Lock spec-driven, AI-first workflow

## Response snapshot

# Implementation Plan: Phase IV - Local Kubernetes Deployment

**Branch**: `001-k8s-minikube-deploy` | **Date**: 2026-02-07 | **Spec**: [D:/phase-three/specs/001-k8s-minikube-deploy/spec.md](file:///D:/phase-three/specs/001-k8s-minikube-deploy/spec.md)
**Input**: Feature specification from `/specs/001-k8s-minikube-deploy/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Deploy the existing Todo Chatbot application to a local Minikube Kubernetes cluster using AI-assisted tools. The approach involves containerizing the frontend and backend services with Docker, creating Helm charts for deployment packaging, and managing the deployment lifecycle using AI tools like Gordon, kubectl-ai, and Kagent without manual coding.

## Technical Context

**Language/Version**: Docker, Kubernetes, Helm
**Primary Dependencies**: Docker Desktop, Minikube, Helm, kubectl, Gordon, kubectl-ai, Kagent
**Storage**: N/A (existing Neon database from Phase III)
**Testing**: Manual validation of deployment success and functionality
**Target Platform**: Local Kubernetes cluster (Minikube)
**Project Type**: Infrastructure/Deployment
**Performance Goals**: Deploy both frontend and backend services within 10 minutes
**Constraints**: Local resource limitations, must use AI-assisted tools only
**Scale/Scope**: Single Todo Chatbot application deployment with both frontend and backend services

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ AI-Driven Infrastructure Automation: All operations must use AI-assisted tools (Gordon, kubectl-ai, Kagent)
- ✅ Container-First Architecture: Applications must be containerized using Docker
- ✅ Spec-Driven Deployment Strategy: Following the Spec → Plan → Tasks → AI Implementation workflow
- ✅ Agent-Driven Execution for Infrastructure: Using Claude Code and AI agents for all operations
- ✅ Local Kubernetes Validation: Deployment to local Minikube cluster as required
- ✅ AI-Assisted DevOps Practices: Using AI tools for all DevOps operations
- ✅ Reusable and Scalable Helm Charts: Creating Helm charts for deployment packaging
- ✅ Zero-Cost Local Environment Priority: Using local Minikube and Docker Desktop

**Post-design evaluation**: All constitutional principles are satisfied by the planned implementation approach. The design includes Dockerfiles for containerization, Helm charts for packaging, and clearly specifies the use of AI tools for all operations.

## Project Structure

### Documentation (this feature)

```text
specs/001-k8s-minikube-deploy/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Infrastructure deployment files
deployment/
├── docker/
│   ├── frontend.Dockerfile
│   └── backend.Dockerfile
├── helm/
│   └── todo-chatbot/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── frontend-deployment.yaml
│           ├── backend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── backend-service.yaml
│           └── ingress.yaml
└── k8s/
    ├── frontend-deployment.yaml
    ├── backend-deployment.yaml
    ├── frontend-service.yaml
    └── backend-service.yaml
```

**Structure Decision**: Single deployment project with separate directories for Dockerfiles, Helm charts, and raw Kubernetes manifests. This structure separates infrastructure concerns and enables both direct Kubernetes deployment and Helm-based deployment.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|

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

# Data Model: Phase IV - Local Kubernetes Deployment

## Overview
This document describes the key entities involved in the Kubernetes deployment of the Todo Chatbot application. Since this is an infrastructure deployment feature, the entities relate to Kubernetes resources and deployment artifacts rather than application data models.

## Key Entities

### Deployment
**Description**: Kubernetes resource defining the desired state for running application containers
- **Attributes**:
  - replicas (int): Number of pod instances to maintain
  - image (string): Container image reference
  - resources (object): CPU and memory limits/requests
  - env (array): Environment variables for the container
  - ports (array): Port mappings for the container
  - livenessProbe (object): Health check configuration
  - readinessProbe (object): Readiness check configuration

### Service
**Description**: Kubernetes resource providing network access to deployed pods
- **Attributes**:
  - type (string): Service type (ClusterIP, NodePort, LoadBalancer)
  - selector (object): Labels to match pods
  - ports (array): Port exposed by the service
  - clusterIP (string): Internal IP address (if applicable)

### Helm Chart
**Description**: Package format for Kubernetes applications containing templates and configuration
- **Attributes**:
  - name (string): Chart name
  - version (string): Chart version
  - description (string): Chart description
  - dependencies (array): Chart dependencies
  - templates (array): Kubernetes manifest templates
  - values (object): Default configuration values

### Container Image
**Description**: Packaged application artifacts stored in Docker registry for deployment
- **Attributes**:
  - repository (string): Image repository name
  - tag (string): Image version tag
  - digest (string): Image checksum
  - size (int): Image size in bytes

## Relationships
- A Helm Chart contains multiple Deployment and Service resources
- A Deployment manages multiple Pod instances
- A Service exposes a Deployment to network traffic
- Container Images are referenced by Deployments

## Validation Rules
- Deployment resource requests must not exceed limits
- Service selectors must match labels on target Deployments
- Helm chart values must be valid YAML
- Container image tags must follow semantic versioning

## State Transitions
- Deployment: Pending → Running → Terminated
- Service: Creating → Active → Deleting
- Helm Release: Deployed → Upgraded → Deleted
- Pod: Pending → Running → Succeeded/Terminated

# Quickstart Guide: Phase IV - Local Kubernetes Deployment

## Prerequisites

Before deploying the Todo Chatbot application to your local Kubernetes cluster, ensure you have the following tools installed:

- Docker Desktop (with Kubernetes enabled) or Docker Engine + kubectl
- Minikube
- Helm v3
- kubectl
- Gordon (Docker AI assistant)
- kubectl-ai (AI-enhanced kubectl)
- Kagent (Kubernetes AI agent)

## Setup Instructions

### 1. Start Minikube Cluster

```bash
minikube start
```

### 2. Clone the Repository

```bash
# If you haven't already cloned the repository
git clone [repository-url]
cd [repository-name]
```

### 3. Prepare the Application

The Todo Chatbot application consists of two parts:
- **Frontend**: Next.js application in the `./frontend` directory
- **Backend**: FastAPI application in the `./backend` directory

### 4. Containerize the Applications using Gordon

#### For the Backend:
```bash
cd ./backend
gordon create-dockerfile
```

#### For the Frontend:
```bash
cd ../frontend
gordon create-dockerfile
```

### 5. Build and Tag Docker Images

```bash
# Build backend image
docker build -t todo-chatbot-backend:latest ./backend

# Build frontend image
docker build -t todo-chatbot-frontend:latest ./frontend
```

### 6. Create Helm Chart

```bash
helm create todo-chatbot
```

### 7. Deploy Using Helm

```bash
helm install todo-chatbot ./todo-chatbot
```

## AI-Assisted Deployment Commands

Instead of manual commands, you can use AI-assisted tools:

### Using kubectl-ai:
```bash
# Get cluster status
kubectl-ai "show me the status of my cluster"

# Check running pods
kubectl-ai "show me all pods in the default namespace"
```

### Using Kagent:
```bash
# Scale the backend deployment
kagent "scale backend deployment to 3 replicas"
```

## Verify Deployment

### 1. Check Running Pods:
```bash
kubectl get pods
```

### 2. Check Services:
```bash
kubectl get services
```

### 3. Access the Application:
```bash
minikube service todo-chatbot-frontend --url
```

## Troubleshooting

### Common Issues:

1. **Pods stuck in Pending state**: Check if Minikube has sufficient resources allocated
2. **Service not accessible**: Verify that the ports are correctly configured
3. **ImagePullBackOff**: Ensure the Docker images are built and tagged correctly

### AI-Assisted Troubleshooting:
```bash
kubectl-ai "describe pods and show me any issues"
```

## Clean Up

To remove the deployment:
```bash
helm uninstall todo-chatbot
```

To stop Minikube:
```bash
minikube stop
```

## Next Steps

Once the deployment is successful, you can:
- Configure ingress to access the application at specific URLs
- Set up persistent storage for the database
- Configure environment variables for the applications
- Implement health checks and readiness probes

## Outcome

- ✅ Impact: Created comprehensive plan for deploying Todo Chatbot to local Kubernetes using AI-assisted tools
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contracts/deployment-api.yaml
- 🔁 Next prompts: Proceed with task breakdown (/sp.tasks) to implement the deployment plan
- 🧠 Reflection: Plan successfully captures the requirements for deploying the existing Todo Chatbot application to Kubernetes using AI-assisted tools, with proper architecture decisions and documentation for implementation

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Break down the implementation into specific tasks using /sp.tasks