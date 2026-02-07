#!/bin/bash

# Script to scale cloud-native architecture services
# This script demonstrates AI-assisted scaling capabilities with kubectl-ai

set -e  # Exit on any error

echo "⚖️  Scaling Cloud-Native Architecture Services..."

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
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first."
    exit 1
fi

echo "✅ Kubernetes cluster is accessible"

# Check for kubectl-ai (AI-assisted kubectl)
if command_exists kubectl-ai; then
    echo "🤖 kubectl-ai found! Using AI-assisted scaling commands..."
    USE_KCTL_AI=true
else
    echo "⚠️  kubectl-ai not found. Using standard kubectl commands..."
    USE_KCTL_AI=false
fi

# Get current replica counts
echo ""
echo "📋 Current Replica Counts:"

# Find backend deployment name
BACKEND_DEPLOYMENT=$(kubectl get deployment | grep -E "(backend-service|.*-backend)" | head -1 | awk '{print $1}')
FRONTEND_DEPLOYMENT=$(kubectl get deployment | grep -E "(frontend-service|.*-frontend)" | head -1 | awk '{print $1}')

if [ -n "$BACKEND_DEPLOYMENT" ]; then
    CURRENT_BACKEND_REPLICAS=$(kubectl get deployment "$BACKEND_DEPLOYMENT" -o jsonpath='{.spec.replicas}')
    echo "📊 Current $BACKEND_DEPLOYMENT replicas: $CURRENT_BACKEND_REPLICAS"
else
    echo "❌ No backend deployment found to scale"
    exit 1
fi

if [ -n "$FRONTEND_DEPLOYMENT" ]; then
    CURRENT_FRONTEND_REPLICAS=$(kubectl get deployment "$FRONTEND_DEPLOYMENT" -o jsonpath='{.spec.replicas}')
    echo "📊 Current $FRONTEND_DEPLOYMENT replicas: $CURRENT_FRONTEND_REPLICAS"
else
    echo "❌ No frontend deployment found to scale"
    exit 1
fi

echo ""

# Parse command line arguments for scaling
BACKEND_SCALE=${1:-$((CURRENT_BACKEND_REPLICAS * 2))}  # Default to doubling backend replicas
FRONTEND_SCALE=${2:-$((CURRENT_FRONTEND_REPLICAS * 2))}  # Default to doubling frontend replicas

echo "📈 Scaling to requested values:"
echo "   Backend: $BACKEND_SCALE replicas"
echo "   Frontend: $FRONTEND_SCALE replicas"

# Scale backend service
echo ""
echo "🔧 Scaling Backend Service..."
if [ "$USE_KCTL_AI" = true ]; then
    kubectl-ai scale deployment "$BACKEND_DEPLOYMENT" --replicas="$BACKEND_SCALE"
else
    kubectl scale deployment "$BACKEND_DEPLOYMENT" --replicas="$BACKEND_SCALE"
fi
echo "✅ Backend service scaled to $BACKEND_SCALE replicas"

# Scale frontend service
echo "🔧 Scaling Frontend Service..."
if [ "$USE_KCTL_AI" = true ]; then
    kubectl-ai scale deployment "$FRONTEND_DEPLOYMENT" --replicas="$FRONTEND_SCALE"
else
    kubectl scale deployment "$FRONTEND_DEPLOYMENT" --replicas="$FRONTEND_SCALE"
fi
echo "✅ Frontend service scaled to $FRONTEND_SCALE replicas"

# Wait for scaling to complete
echo ""
echo "⏱️  Waiting for scaling to complete..."

# Wait for backend
kubectl wait --for=condition=available deployment/"$BACKEND_DEPLOYMENT" --timeout=300s
echo "✅ Backend scaling completed"

# Wait for frontend
kubectl wait --for=condition=available deployment/"$FRONTEND_DEPLOYMENT" --timeout=300s
echo "✅ Frontend scaling completed"

# Show new status
echo ""
echo "📊 New Deployment Status:"
kubectl get deployments

# Verify scaled pods are running
echo ""
echo "📋 Running Pods After Scaling:"
kubectl get pods

# Optional: Show resource usage
echo ""
echo "📈 Resource Usage After Scaling:"
kubectl top pods 2>/dev/null || echo "⚠️  Metrics server not available - install metrics server for resource monitoring"

echo ""
echo "🎉 Service scaling completed successfully!"
echo ""
echo "📊 Scaling Summary:"
echo "   - Backend: $CURRENT_BACKEND_REPLICAS → $BACKEND_SCALE replicas"
echo "   - Frontend: $CURRENT_FRONTEND_REPLICAS → $FRONTEND_SCALE replicas"
echo ""
echo "💡 Tip: Use 'kubectl get hpa' if you have configured Horizontal Pod Autoscalers for automatic scaling!"
echo "📝 Next: Monitor performance to ensure scaled services are functioning properly."