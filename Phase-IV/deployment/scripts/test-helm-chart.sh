#!/bin/bash

# Script to test Helm chart deployment to Minikube
# This script assumes Minikube is running and kubectl is configured

set -e  # Exit on any error

echo "🧪 Testing Helm Chart Deployment..."

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo "❌ Helm is not installed. Please install Helm first."
    echo "Installation instructions: https://helm.sh/docs/intro/install/"
    exit 1
fi

# Check if Minikube is running
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first:"
    echo "minikube start"
    exit 1
fi

echo "✅ Prerequisites verified: Helm installed and cluster accessible"

# Navigate to Helm chart directory
cd deployment/helm/todo-chatbot

echo "📝 Installing Helm chart..."
helm install todo-chatbot . --values values.yaml --wait --timeout=10m

echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-chatbot-backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=todo-chatbot-frontend --timeout=300s

echo "🔍 Checking service status..."
kubectl get services

echo "🌐 Testing service accessibility..."
BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}')
FRONTEND_POD=$(kubectl get pods -l app=todo-chatbot-frontend -o jsonpath='{.items[0].metadata.name}')

echo "Backend pod: $BACKEND_POD"
echo "Frontend pod: $FRONTEND_POD"

echo "✅ Helm chart deployed successfully!"
echo ""
echo "📊 Deployment Summary:"
echo "   - Backend deployment: todo-chatbot-backend"
echo "   - Frontend deployment: todo-chatbot-frontend"
echo "   - Backend service: ClusterIP (internal access)"
echo "   - Frontend service: LoadBalancer (external access)"
echo ""
echo "🚀 To access the application:"
echo "   - Run: minikube service todo-chatbot-frontend-service"
echo "   - Or check external IP: kubectl get services"
echo ""
echo "🔧 To customize deployment, edit values.yaml and upgrade:"
echo "   - helm upgrade todo-chatbot . --values values.yaml"
echo ""
echo "🧹 To uninstall:"
echo "   - helm uninstall todo-chatbot"