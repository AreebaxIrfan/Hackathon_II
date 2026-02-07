# Cloud-Native Kubernetes Architecture - Infrastructure

## Overview

This directory contains all the infrastructure code and configuration for deploying the application to a local Kubernetes cluster using Minikube.

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
infrastructure/
├── docker/              # Dockerfiles for containerization
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── kubernetes/          # Kubernetes manifests
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   └── frontend-service.yaml
└── helm/                # Helm charts
    └── cloud-native-arch/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
```

## Quick Start

### 1. Start Minikube

```bash
minikube start --cpus=4 --memory=8192
```

### 2. Build Docker Images

```bash
# Backend
docker build -f infrastructure/docker/backend.Dockerfile -t backend-service:latest .

# Frontend
docker build -f infrastructure/docker/frontend.Dockerfile -t frontend-service:latest .
```

### 3. Load Images into Minikube

```bash
minikube image load backend-service:latest
minikube image load frontend-service:latest
```

### 4. Deploy to Kubernetes

```bash
kubectl apply -f infrastructure/kubernetes/
```

### 5. Deploy Using Helm (Alternative Approach)

```bash
helm install cloud-native-app infrastructure/helm/cloud-native-arch/ --values infrastructure/helm/cloud-native-arch/values.yaml
```

## Architecture Principles

This implementation follows cloud-native architecture principles:

- Microservices with loose coupling
- Container-based deployment
- Declarative configuration
- Infrastructure as code
- Self-healing capabilities
- Service discovery and load balancing
- Resource isolation and allocation

## Components

### Frontend Service
- Containerized web application
- Kubernetes deployment and service
- Health checks and readiness probes
- Resource allocation limits

### Backend Service
- Containerized API server
- Kubernetes deployment and service
- Health checks and readiness probes
- Resource allocation limits
- Service discovery configuration

### Service Communication
- Internal communication via Kubernetes DNS
- Load balancing through Kubernetes services
- Network policies for security (optional)

## Deployment Methods

### Method 1: Direct kubectl (User Story 1)
Use raw Kubernetes manifests with kubectl commands.

### Method 2: AI-Assisted Management (User Story 2)
Use kubectl-ai and Kagent for intelligent cluster management.

### Method 3: Helm Charts (User Story 3)
Use Helm for parameterized, reusable deployments.

## Configuration

Configuration is managed through:

- Kubernetes ConfigMaps and Secrets
- Helm values files for customizable parameters
- Environment variables for service-specific settings

## Next Steps

1. Complete Phase 1: Setup ✓
2. Complete Phase 2: Foundational (AI tools setup)
3. Implement User Story 1: Containerize services
4. Implement User Story 2: Deploy to Kubernetes
5. Implement User Story 3: Helm chart deployment
6. Implement User Story 4: Architecture validation

## References

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- Project Quickstart: `../specs/001-sp-02-architecture-specification-the-system-follows-a-cloud-native-architecture-consisting-of-a-frontend-and-backend-service-both-services-run-as-containerized-applications-inside-a-local-kubernetes-cluster-minikube-acts-as-the-orchestratio/quickstart.md`