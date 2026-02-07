#!/bin/bash

# Script to deploy cloud-native architecture to Kubernetes
# This script handles deployment using both kubectl and Helm

set -e  # Exit on any error

echo "🚀 Deploying Cloud-Native Architecture to Kubernetes..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for kubectl
if ! command_exists kubectl; then
    echo "❌ kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first:"
    echo "   minikube start --cpus=4 --memory=8192"
    exit 1
fi

echo "✅ Kubernetes cluster is accessible"

# Check for kubectl-ai (AI-assisted kubectl)
if command_exists kubectl-ai; then
    echo "🤖 kubectl-ai found! Using AI-assisted kubectl commands..."
    USE_KCTL_AI=true
else
    echo "⚠️  kubectl-ai not found. Using standard kubectl commands..."
    USE_KCTL_AI=false
fi

# Option to deploy using raw Kubernetes manifests or Helm
DEPLOY_METHOD=${1:-"k8s"}  # Default to k8s, can be overridden with "helm"

if [ "$DEPLOY_METHOD" = "k8s" ]; then
    echo "📊 Deploying using Kubernetes manifests..."

    # Apply backend first
    echo "📦 Deploying Backend Service..."
    if [ "$USE_KCTL_AI" = true ]; then
        kubectl-ai apply -f infrastructure/kubernetes/backend-deployment.yaml
        kubectl-ai apply -f infrastructure/kubernetes/backend-service.yaml
    else
        kubectl apply -f infrastructure/kubernetes/backend-deployment.yaml
        kubectl apply -f infrastructure/kubernetes/backend-service.yaml
    fi

    # Wait for backend to be ready
    echo "⏱️  Waiting for Backend Service to be ready..."
    kubectl wait --for=condition=ready pod -l app=backend-service --timeout=300s

    # Apply frontend
    echo "📦 Deploying Frontend Service..."
    if [ "$USE_KCTL_AI" = true ]; then
        kubectl-ai apply -f infrastructure/kubernetes/frontend-deployment.yaml
        kubectl-ai apply -f infrastructure/kubernetes/frontend-service.yaml
    else
        kubectl apply -f infrastructure/kubernetes/frontend-deployment.yaml
        kubectl apply -f infrastructure/kubernetes/frontend-service.yaml
    fi

    echo "✅ Kubernetes manifests deployed successfully!"

elif [ "$DEPLOY_METHOD" = "helm" ]; then
    echo "📦 Deploying using Helm Chart..."

    # Check for Helm
    if ! command_exists helm; then
        echo "❌ Helm not found. Please install Helm first."
        exit 1
    fi

    # Check if release already exists
    if helm list --short | grep -q "^cloud-native-app$"; then
        echo "🔄 Helm release exists. Upgrading..."
        if command_exists kubectl-ai && [ "$USE_KCTL_AI" = true ]; then
            kubectl-ai upgrade --install cloud-native-app infrastructure/helm/cloud-native-arch/ --values infrastructure/helm/cloud-native-arch/values.yaml
        else
            helm upgrade --install cloud-native-app infrastructure/helm/cloud-native-arch/ --values infrastructure/helm/cloud-native-arch/values.yaml
        fi
    else
        echo "🎨 Installing Helm release..."
        if command_exists kubectl-ai && [ "$USE_KCTL_AI" = true ]; then
            kubectl-ai install cloud-native-app infrastructure/helm/cloud-native-arch/ --values infrastructure/helm/cloud-native-arch/values.yaml
        else
            helm install cloud-native-app infrastructure/helm/cloud-native-arch/ --values infrastructure/helm/cloud-native-arch/values.yaml
        fi
    fi

    echo "✅ Helm chart deployed successfully!"
fi

# Wait for all deployments to be ready
echo "⏱️  Waiting for all deployments to be ready..."
kubectl wait --for=condition=available deployment/backend-service --timeout=300s || kubectl wait --for=condition=available deployment/cloud-native-app-backend --timeout=300s
kubectl wait --for=condition=available deployment/frontend-service --timeout=300s || kubectl wait --for=condition=available deployment/cloud-native-app-frontend --timeout=300s

# Show deployment status
echo "📋 Deployment Status:"
kubectl get deployments
kubectl get services
kubectl get pods

echo ""
echo "🎉 Cloud-Native Architecture deployment completed!"
echo ""
echo "📊 Deployment Method: $DEPLOY_METHOD"
echo "   To access the application, run: minikube service frontend-service --url"
echo "   Or for Helm: minikube service cloud-native-app-frontend-service --url"
echo ""
echo "🔍 To monitor: kubectl get pods --watch"
echo "🔧 To check logs: kubectl logs -l app=frontend-service"
echo ""
echo "💡 Tip: Use 'kubectl get events' to see any deployment issues if needed."