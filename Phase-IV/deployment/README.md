# Phase IV: Local Kubernetes Deployment

## Overview

This directory contains all the infrastructure code and configuration for deploying the Todo Chatbot application to a local Kubernetes cluster using Minikube.

## Prerequisites

- Docker Desktop (v29.1.5 or later)
- Minikube (v1.38.0 or later)
- Helm v3 (required for Helm-based deployment)
- kubectl CLI tool
- AI-assisted tools (optional but recommended):
  - Gordon (Docker AI)
  - kubectl-ai
  - Kagent

## Directory Structure

```
deployment/
├── docker/              # Dockerfiles for containerization
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── k8s/                 # Kubernetes manifests
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   └── frontend-service.yaml
└── helm/                # Helm charts
    └── todo-chatbot/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
```

## Quick Start

### 1. Start Minikube

```bash
minikube start --cpus=4 --memory=4096
```

### 2. Build Docker Images

```bash
# Backend
docker build -f deployment/docker/backend.Dockerfile -t todo-backend:latest ./backend

# Frontend
docker build -f deployment/docker/frontend.Dockerfile -t todo-frontend:latest ./frontend
```

### 3. Load Images into Minikube

```bash
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### 4. Deploy to Kubernetes

```bash
kubectl apply -f deployment/k8s/
```

### 5. Verify Deployment

```bash
kubectl get pods
kubectl get services
```

### 6. Access the Application

```bash
# Get the frontend service URL
minikube service frontend-service --url
```

## Deployment Methods

### Method 1: Direct kubectl (User Story 1)
Use raw Kubernetes manifests with kubectl commands.

### Method 2: AI-Assisted Management (User Story 2)
Use kubectl-ai and Kagent for intelligent cluster management.

### Method 3: Helm Charts (User Story 3)
Use Helm for parameterized, reusable deployments.

#### Helm Chart Deployment

The Helm chart for the Todo Chatbot application is located in `deployment/helm/todo-chatbot/`. This chart packages both the frontend and backend services with configurable parameters.

To install the Helm chart:
```bash
cd deployment/helm/todo-chatbot/
helm install todo-chatbot . --values values.yaml
```

To test the Helm chart deployment (when Minikube is running):
```bash
./deployment/scripts/test-helm-chart.sh
```

To verify configuration parameter customization:
```bash
./deployment/scripts/verify-helm-config.sh
```

For more details, see the Helm chart README in `deployment/helm/todo-chatbot/README.md`.

## Troubleshooting

### Minikube Issues

**Permission Errors (Hyper-V)**:
- Run PowerShell as Administrator
- Ensure Hyper-V is enabled in Windows Features
- Check that your user is in the Hyper-V Administrators group

**Resource Issues**:
```bash
minikube start --cpus=4 --memory=4096 --disk-size=20g
```

### Pod Issues

**ImagePullBackOff**:
- Ensure images are loaded into Minikube: `minikube image load <image-name>`
- Check image names match in deployment manifests

**CrashLoopBackOff**:
- Check pod logs: `kubectl logs <pod-name>`
- Verify environment variables and configuration

### Service Issues

**Service Not Accessible**:
- Use `minikube service <service-name> --url` to get the correct URL
- Check service selectors match pod labels

## Environment Variables

Required environment variables for the application:

**Backend**:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI functionality
- `BETTER_AUTH_SECRET`: Authentication secret

**Frontend**:
- `NEXT_PUBLIC_API_URL`: Backend API URL

## Health Checks

Both services include health check endpoints:
- Backend: `GET /health`
- Frontend: `GET /api/health`

## Resource Limits

Default resource allocations:

**Backend**:
- CPU: 500m request, 1000m limit
- Memory: 512Mi request, 1Gi limit

**Frontend**:
- CPU: 200m request, 500m limit
- Memory: 256Mi request, 512Mi limit

## Next Steps

1. Complete Phase 1: Setup ✓
2. Complete Phase 2: Foundational ✓
3. Implement User Story 1: Basic Kubernetes deployment ✓
4. Implement User Story 2: AI-assisted management ✓
5. Implement User Story 3: Helm chart deployment ✓
6. Implement User Story 4: Validation and testing ✓

## Deployment Procedures

### Quick Deployment (Using Helm - Recommended)

The easiest way to deploy the Todo Chatbot application is using the Helm chart:

1. Ensure Minikube is running:
   ```bash
   minikube start --cpus=4 --memory=4096
   ```

2. Navigate to the Helm chart directory:
   ```bash
   cd deployment/helm/todo-chatbot/
   ```

3. Install the Helm chart:
   ```bash
   helm install todo-chatbot . --values values.yaml
   ```

4. Wait for pods to be ready:
   ```bash
   kubectl get pods --watch
   ```

5. Access the application:
   ```bash
   minikube service todo-chatbot-frontend-service --url
   ```

### Manual Deployment (Using Raw Kubernetes Manifests)

If you prefer to use raw Kubernetes manifests:

1. Build Docker images:
   ```bash
   docker build -f deployment/docker/backend.Dockerfile -t todo-backend:latest ./backend
   docker build -f deployment/docker/frontend.Dockerfile -t todo-frontend:latest ./frontend
   ```

2. Load images into Minikube:
   ```bash
   minikube image load todo-backend:latest
   minikube image load todo-frontend:latest
   ```

3. Apply Kubernetes manifests:
   ```bash
   kubectl apply -f deployment/k8s/
   ```

4. Access the application:
   ```bash
   minikube service frontend-service --url
   ```

## References

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- Project Quickstart: `../specs/001-k8s-minikube-deploy/quickstart.md`
