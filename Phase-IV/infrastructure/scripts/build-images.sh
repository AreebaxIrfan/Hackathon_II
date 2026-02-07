#!/bin/bash

# Script to build Docker images for frontend and backend services
# This script uses Gordon AI (if available) or standard Docker commands

set -e  # Exit on any error

echo "🏗️  Building Docker Images for Cloud-Native Architecture..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Gordon (Docker AI tool) - use it if available
if command_exists gordon; then
    echo "🤖 Gordon (Docker AI) found! Using AI-assisted Docker commands..."
    USE_GORDON=true
else
    echo "⚠️  Gordon not found. Using standard Docker commands..."
    USE_GORDON=false
fi

# Build backend image
echo "📦 Building Backend Service Image..."
if [ "$USE_GORDON" = true ]; then
    # Using Gordon for AI-assisted Docker build
    gordon build -f infrastructure/docker/backend.Dockerfile -t backend-service:latest .
else
    # Using standard Docker
    docker build -f infrastructure/docker/backend.Dockerfile -t backend-service:latest .
fi

echo "✅ Backend image built successfully!"

# Build frontend image
echo "📦 Building Frontend Service Image..."
if [ "$USE_GORDON" = true ]; then
    # Using Gordon for AI-assisted Docker build
    gordon build -f infrastructure/docker/frontend.Dockerfile -t frontend-service:latest .
else
    # Using standard Docker
    docker build -f infrastructure/docker/frontend.Dockerfile -t frontend-service:latest .
fi

echo "✅ Frontend image built successfully!"

# Show built images
echo "📋 Built Images:"
docker images | grep -E "(backend-service|frontend-service)"

echo ""
echo "🎉 Docker image build process completed!"
echo ""
echo "📝 Next steps:"
echo "   1. Load images into Minikube: minikube image load backend-service:latest"
echo "   2. Load images into Minikube: minikube image load frontend-service:latest"
echo "   3. Deploy to Kubernetes: kubectl apply -f infrastructure/kubernetes/"
echo ""
echo "💡 Tip: Use the deploy script to automate the full deployment process!"