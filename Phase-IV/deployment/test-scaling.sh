#!/bin/bash
# Test scaling deployments using kubectl-ai (or standard kubectl)

set -e

echo "=== Testing Kubernetes Scaling Operations ==="
echo ""

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster not accessible"
    exit 1
fi

echo "✓ Kubernetes cluster is accessible"
echo ""

# Function to scale deployment
scale_deployment() {
    local deployment=$1
    local replicas=$2

    echo "Scaling $deployment to $replicas replicas..."

    # Try kubectl-ai first, fallback to standard kubectl
    if command -v kubectl-ai &> /dev/null; then
        kubectl-ai "scale $deployment to $replicas replicas"
    else
        kubectl scale deployment/$deployment --replicas=$replicas
    fi

    # Wait for scaling to complete
    kubectl wait --for=condition=available --timeout=120s deployment/$deployment

    # Verify scaling
    CURRENT_REPLICAS=$(kubectl get deployment $deployment -o jsonpath='{.status.readyReplicas}')
    if [ "$CURRENT_REPLICAS" -eq "$replicas" ]; then
        echo "✓ $deployment scaled successfully to $replicas replicas"
    else
        echo "❌ Scaling failed. Current replicas: $CURRENT_REPLICAS, Expected: $replicas"
        return 1
    fi

    echo ""
}

# Test backend scaling
echo "=== Testing Backend Scaling ==="
echo ""

# Scale up
scale_deployment "backend-deployment" 2

# Show pod distribution
echo "Backend pods:"
kubectl get pods -l app=todo-backend -o wide

echo ""

# Scale down
scale_deployment "backend-deployment" 1

echo ""

# Test frontend scaling
echo "=== Testing Frontend Scaling ==="
echo ""

# Scale up
scale_deployment "frontend-deployment" 3

# Show pod distribution
echo "Frontend pods:"
kubectl get pods -l app=todo-frontend -o wide

echo ""

# Scale down
scale_deployment "frontend-deployment" 1

echo ""
echo "=== Scaling Tests Complete ==="
echo ""

# Show final state
echo "Final Deployment State:"
kubectl get deployments

echo ""
echo "Resource Usage:"
if command -v kubectl &> /dev/null; then
    kubectl top pods 2>/dev/null || echo "Metrics server not available"
fi
