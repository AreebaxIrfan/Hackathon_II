#!/bin/bash
# Deploy Todo Chatbot to Minikube cluster

set -e

echo "=== Todo Chatbot Kubernetes Deployment ==="
echo ""

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster not accessible"
    echo "   Please start Minikube: minikube start --cpus=4 --memory=4096"
    exit 1
fi

echo "✓ Kubernetes cluster is accessible"
echo ""

# Check if images exist
echo "Checking Docker images..."
if ! docker images | grep -q "todo-backend"; then
    echo "❌ Backend image not found. Please run: ./deployment/build-images.sh"
    exit 1
fi

if ! docker images | grep -q "todo-frontend"; then
    echo "❌ Frontend image not found. Please run: ./deployment/build-images.sh"
    exit 1
fi

echo "✓ Docker images found"
echo ""

# Load images into Minikube
echo "Loading images into Minikube..."
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
echo "✓ Images loaded into Minikube"
echo ""

# Check if secrets exist
echo "Checking for secrets..."
if ! kubectl get secret database-secret &> /dev/null; then
    echo "⚠ Secrets not found. Creating secrets..."
    ./deployment/create-secrets.sh
else
    echo "✓ Secrets already exist"
fi

echo ""
echo "Deploying to Kubernetes..."

# Apply Kubernetes manifests
kubectl apply -f deployment/k8s/backend-deployment.yaml
kubectl apply -f deployment/k8s/backend-service.yaml
kubectl apply -f deployment/k8s/frontend-deployment.yaml
kubectl apply -f deployment/k8s/frontend-service.yaml

echo ""
echo "✓ Manifests applied"
echo ""

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/backend-deployment
kubectl wait --for=condition=available --timeout=300s deployment/frontend-deployment

echo ""
echo "=== Deployment Complete ==="
echo ""

# Show deployment status
echo "Deployment Status:"
kubectl get deployments
echo ""

echo "Pod Status:"
kubectl get pods
echo ""

echo "Service Status:"
kubectl get services
echo ""

echo "To access the frontend:"
echo "minikube service frontend-service --url"
echo ""

echo "To check logs:"
echo "kubectl logs -l app=todo-backend"
echo "kubectl logs -l app=todo-frontend"
