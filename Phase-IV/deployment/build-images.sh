#!/bin/bash
# Build Docker images for Todo Chatbot deployment

set -e

echo "=== Building Todo Chatbot Docker Images ==="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Build backend image
echo "Building backend image..."
docker build -f deployment/docker/backend.Dockerfile -t todo-backend:latest ./backend

if [ $? -eq 0 ]; then
    echo "✓ Backend image built successfully"
else
    echo "❌ Backend image build failed"
    exit 1
fi

echo ""

# Build frontend image
echo "Building frontend image..."
docker build -f deployment/docker/frontend.Dockerfile -t todo-frontend:latest ./frontend

if [ $? -eq 0 ]; then
    echo "✓ Frontend image built successfully"
else
    echo "❌ Frontend image build failed"
    exit 1
fi

echo ""
echo "=== Build Complete ==="
echo ""
echo "Images created:"
docker images | grep todo-

echo ""
echo "Next steps:"
echo "1. Load images into Minikube: ./deployment/load-images-to-minikube.sh"
echo "2. Deploy to Kubernetes: kubectl apply -f deployment/k8s/"
