# Quickstart Guide: Cloud-Native Kubernetes Architecture

## Overview
This guide will help you quickly set up and deploy the cloud-native architecture with frontend and backend services in a local Kubernetes cluster using Minikube.

## Prerequisites
- Docker Desktop (v29.1.5 or later)
- Minikube (v1.38.0 or later)
- kubectl CLI tool
- Helm v3.x
- Git

## Step 1: Start Minikube
```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Verify Minikube is running
minikube status
```

## Step 2: Prepare Your Application Code
```bash
# Clone your application repository (replace with actual repository)
git clone <your-application-repo>
cd <your-application-directory>

# Ensure your frontend and backend code are available in the respective directories
# Frontend code should be in the 'frontend' directory
# Backend code should be in the 'backend' directory
```

## Step 3: Build Container Images
```bash
# Build frontend container image
docker build -f Dockerfile.frontend -t frontend-app:latest ./frontend

# Build backend container image
docker build -f Dockerfile.backend -t backend-app:latest ./backend

# Load images into Minikube
minikube image load frontend-app:latest
minikube image load backend-app:latest
```

## Step 4: Create Namespace (Optional)
```bash
# Create a dedicated namespace for your application
kubectl create namespace cloud-native-app
kubectl config set-context --current --namespace=cloud-native-app
```

## Step 5: Deploy to Kubernetes
```bash
# Create deployments and services using kubectl
kubectl apply -f k8s/frontend-deployment.yaml
kubectl apply -f k8s/frontend-service.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/backend-service.yaml
```

## Step 6: Deploy Using Helm (Alternative Approach)
```bash
# Navigate to Helm chart directory
cd helm/cloud-native-arch-chart

# Install the Helm chart
helm install cloud-native-app . --values values.yaml --wait

# Or upgrade if already installed
helm upgrade --install cloud-native-app . --values values.yaml --wait
```

## Step 7: Verify Deployment
```bash
# Check if pods are running
kubectl get pods

# Check if services are available
kubectl get services

# Check deployment status
kubectl get deployments
```

## Step 8: Access the Application
```bash
# Get the frontend service URL
minikube service frontend-service --url

# Or use the tunnel command for persistent access
minikube tunnel

# Alternatively, you can port forward to access locally
kubectl port-forward service/frontend-service 3000:3000
```

## Step 9: Scale Services (Optional)
```bash
# Scale frontend deployment
kubectl scale deployment frontend-service --replicas=3

# Scale backend deployment
kubectl scale deployment backend-service --replicas=2
```

## Step 10: Monitor Services
```bash
# Check pod logs
kubectl logs -l app=frontend-service
kubectl logs -l app=backend-service

# Get resource usage
kubectl top pods
```

## Troubleshooting

### Common Issues:

1. **Images not found**:
   - Ensure images are loaded into Minikube: `minikube image load <image-name>`
   - Check image names match in deployment manifests

2. **Services not accessible**:
   - Use `minikube service <service-name> --url` to get the correct URL
   - Check service selectors match pod labels

3. **Pods in pending state**:
   - Verify Minikube has sufficient resources
   - Check resource limits in deployment manifests

4. **Inter-service communication issues**:
   - Ensure services can reach each other using Kubernetes DNS
   - Check environment variables for service URLs

## Next Steps
- Configure ingress for more sophisticated routing
- Set up monitoring and logging
- Configure persistent storage if needed
- Set up CI/CD pipeline
- Configure security (RBAC, network policies, etc.)

## Cleanup
```bash
# Uninstall Helm release
helm uninstall cloud-native-app

# Or delete resources individually
kubectl delete -f k8s/

# Stop Minikube
minikube stop
```

This quickstart guide provides a basic setup for deploying the cloud-native architecture with frontend and backend services in Kubernetes. Adjust configurations as needed for your specific application requirements.