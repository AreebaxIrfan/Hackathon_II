#!/bin/bash
# Verify Todo Chatbot deployment is working correctly

set -e

echo "=== Todo Chatbot Deployment Verification ==="
echo ""

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster not accessible"
    exit 1
fi

echo "✓ Kubernetes cluster is accessible"
echo ""

# Check deployments
echo "Checking Deployments..."
BACKEND_READY=$(kubectl get deployment backend-deployment -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
FRONTEND_READY=$(kubectl get deployment frontend-deployment -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")

if [ "$BACKEND_READY" -gt 0 ]; then
    echo "✓ Backend deployment is ready ($BACKEND_READY replicas)"
else
    echo "❌ Backend deployment is not ready"
    kubectl get deployment backend-deployment
fi

if [ "$FRONTEND_READY" -gt 0 ]; then
    echo "✓ Frontend deployment is ready ($FRONTEND_READY replicas)"
else
    echo "❌ Frontend deployment is not ready"
    kubectl get deployment frontend-deployment
fi

echo ""

# Check pods
echo "Checking Pods..."
kubectl get pods -l app=todo-backend
kubectl get pods -l app=todo-frontend

echo ""

# Check services
echo "Checking Services..."
kubectl get services backend-service frontend-service

echo ""

# Test backend health endpoint
echo "Testing Backend Health..."
BACKEND_POD=$(kubectl get pod -l app=todo-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -n "$BACKEND_POD" ]; then
    echo "Backend pod: $BACKEND_POD"
    kubectl exec $BACKEND_POD -- curl -s http://localhost:8000/health || echo "❌ Backend health check failed"
else
    echo "❌ No backend pod found"
fi

echo ""

# Test frontend accessibility
echo "Testing Frontend Accessibility..."
FRONTEND_POD=$(kubectl get pod -l app=todo-frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -n "$FRONTEND_POD" ]; then
    echo "Frontend pod: $FRONTEND_POD"
    kubectl exec $FRONTEND_POD -- wget -q -O- http://localhost:3000 > /dev/null && echo "✓ Frontend is responding" || echo "❌ Frontend not responding"
else
    echo "❌ No frontend pod found"
fi

echo ""

# Get frontend URL
echo "Frontend Access URL:"
minikube service frontend-service --url

echo ""

# Check logs for errors
echo "Recent Backend Logs:"
kubectl logs -l app=todo-backend --tail=10

echo ""
echo "Recent Frontend Logs:"
kubectl logs -l app=todo-frontend --tail=10

echo ""
echo "=== Verification Complete ==="
echo ""
echo "To access the application:"
echo "1. Get URL: minikube service frontend-service --url"
echo "2. Open in browser"
echo ""
echo "To monitor:"
echo "kubectl get pods -w"
echo "kubectl logs -f -l app=todo-backend"
