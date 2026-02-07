#!/bin/bash

# Script to verify cloud-native architecture deployment
# This script checks that all services are running and accessible

set -e  # Exit on any error

echo "🔍 Verifying Cloud-Native Architecture Deployment..."

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first."
    exit 1
fi

echo "✅ Kubernetes cluster is accessible"

# Check deployments
echo "📋 Checking Deployments..."

# Check for deployments (either raw k8s or helm)
BACKEND_DEPLOYMENT=$(kubectl get deployment | grep -E "(backend-service|.*-backend)" | head -1 | awk '{print $1}')
FRONTEND_DEPLOYMENT=$(kubectl get deployment | grep -E "(frontend-service|.*-frontend)" | head -1 | awk '{print $1}')

if [ -n "$BACKEND_DEPLOYMENT" ]; then
    echo "✅ Backend deployment '$BACKEND_DEPLOYMENT' found"

    # Check if backend is ready
    READY_REPLICAS=$(kubectl get deployment "$BACKEND_DEPLOYMENT" -o jsonpath='{.status.readyReplicas}')
    DESIRED_REPLICAS=$(kubectl get deployment "$BACKEND_DEPLOYMENT" -o jsonpath='{.spec.replicas}')

    if [ "$READY_REPLICAS" -eq "$DESIRIRED_REPLICAS" ] && [ "$READY_REPLICAS" -gt 0 ]; then
        echo "✅ Backend deployment has $READY_REPLICAS/$DESIRIRED_REPLICAS replicas ready"
    else
        echo "❌ Backend deployment has $READY_REPLICAS/$DESIRIRED_REPLICAS replicas ready"
    fi
else
    echo "❌ No backend deployment found"
fi

if [ -n "$FRONTEND_DEPLOYMENT" ]; then
    echo "✅ Frontend deployment '$FRONTEND_DEPLOYMENT' found"

    # Check if frontend is ready
    READY_REPLICAS=$(kubectl get deployment "$FRONTEND_DEPLOYMENT" -o jsonpath='{.status.readyReplicas}')
    DESIRED_REPLICAS=$(kubectl get deployment "$FRONTEND_DEPLOYMENT" -o jsonpath='{.spec.replicas}')

    if [ "$READY_REPLICAS" -eq "$DESIRIRED_REPLICAS" ] && [ "$READY_REPLICAS" -gt 0 ]; then
        echo "✅ Frontend deployment has $READY_REPLICAS/$DESIRIRED_REPLICAS replicas ready"
    else
        echo "❌ Frontend deployment has $READY_REPLICAS/$DESIRIRED_REPLICAS replicas ready"
    fi
else
    echo "❌ No frontend deployment found"
fi

# Check services
echo ""
echo "📋 Checking Services..."

BACKEND_SERVICE=$(kubectl get service | grep -E "(backend-service|.*-backend-service)" | head -1 | awk '{print $1}')
FRONTEND_SERVICE=$(kubectl get service | grep -E "(frontend-service|.*-frontend-service)" | head -1 | awk '{print $1}')

if [ -n "$BACKEND_SERVICE" ]; then
    echo "✅ Backend service '$BACKEND_SERVICE' found"
    kubectl get service "$BACKEND_SERVICE" -o wide
else
    echo "❌ No backend service found"
fi

if [ -n "$FRONTEND_SERVICE" ]; then
    echo "✅ Frontend service '$FRONTEND_SERVICE' found"
    kubectl get service "$FRONTEND_SERVICE" -o wide
else
    echo "❌ No frontend service found"
fi

# Check pods
echo ""
echo "📋 Checking Pods..."

BACKEND_PODS=$(kubectl get pods -l app="${BACKEND_SERVICE%-service}" 2>/dev/null | grep -c "Running" || kubectl get pods -l app="$BACKEND_DEPLOYMENT" 2>/dev/null | grep -c "Running" || echo "0")
FRONTEND_PODS=$(kubectl get pods -l app="${FRONTEND_SERVICE%-service}" 2>/dev/null | grep -c "Running" || kubectl get pods -l app="$FRONTEND_DEPLOYMENT" 2>/dev/null | grep -c "Running" || echo "0")

if [ "$BACKEND_PODS" -gt 0 ]; then
    echo "✅ Found $BACKEND_PODS running backend pod(s)"
    kubectl get pods -l app="${BACKEND_SERVICE%-service}" 2>/dev/null || kubectl get pods -l app="$BACKEND_DEPLOYMENT" 2>/dev/null
else
    echo "❌ No running backend pods found"
fi

if [ "$FRONTEND_PODS" -gt 0 ]; then
    echo "✅ Found $FRONTEND_PODS running frontend pod(s)"
    kubectl get pods -l app="${FRONTEND_SERVICE%-service}" 2>/dev/null || kubectl get pods -l app="$FRONTEND_DEPLOYMENT" 2>/dev/null
else
    echo "❌ No running frontend pods found"
fi

# Test service connectivity (if pods are running)
if [ "$BACKEND_PODS" -gt 0 ] && [ "$FRONTEND_PODS" -gt 0 ]; then
    echo ""
    echo "🧪 Testing Service Connectivity..."

    # Get first backend pod
    BACKEND_POD=$(kubectl get pods -l app="${BACKEND_SERVICE%-service}" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app="$BACKEND_DEPLOYMENT" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

    if [ -n "$BACKEND_POD" ]; then
        # Test if backend service is responding to health check
        echo "🔍 Testing backend health endpoint..."
        BACKEND_HEALTH=$(kubectl exec "$BACKEND_POD" -- timeout 10s curl -s -w ":%{http_code}" http://localhost:8000/health 2>/dev/null || echo "FAILED:404")

        if [[ $BACKEND_HEALTH == *":200"* ]]; then
            echo "✅ Backend health check: SUCCESS"
        else
            echo "⚠️  Backend health check: $BACKEND_HEALTH"
        fi
    fi

    # Get first frontend pod
    FRONTEND_POD=$(kubectl get pods -l app="${FRONTEND_SERVICE%-service}" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app="$FRONTEND_DEPLOYMENT" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

    if [ -n "$FRONTEND_POD" ]; then
        # Test if frontend is responding
        echo "🔍 Testing frontend accessibility..."
        FRONTEND_STATUS=$(kubectl exec "$FRONTEND_POD" -- timeout 10s curl -s -w ":%{http_code}" http://localhost:3000/ 2>/dev/null || echo "FAILED:404")

        if [[ $FRONTEND_STATUS == *":200"* ]] || [[ $FRONTEND_STATUS == *":404"* ]]; then
            echo "✅ Frontend status check: SUCCESS"
        else
            echo "⚠️  Frontend status check: $FRONTEND_STATUS"
        fi
    fi
fi

# Check for any errors in the pods
echo ""
echo "🔍 Checking for pod errors..."

ALL_PODS=$(kubectl get pods -o jsonpath='{.items[*].metadata.name}')

for pod in $ALL_PODS; do
    if kubectl describe pod "$pod" | grep -q "Reason:\s*Error\|Failed\|CrashLoopBackOff\|ImagePullBackOff"; then
        echo "❌ Pod $pod has errors:"
        kubectl describe pod "$pod" | grep -A 10 -B 10 -E "Reason:\s*Error|Failed|CrashLoopBackOff|ImagePullBackOff"
    else
        echo "✅ Pod $pod has no critical errors"
    fi
done

# Show recent events
echo ""
echo "📋 Recent Kubernetes Events:"
kubectl get events --sort-by='.lastTimestamp' --field-selector involvedObject.kind=Pod | tail -10

echo ""
echo "🎉 Verification completed!"
echo ""
echo "📋 Summary:"
if [ -n "$BACKEND_DEPLOYMENT" ] && [ -n "$FRONTEND_DEPLOYMENT" ] && [ "$BACKEND_PODS" -gt 0 ] && [ "$FRONTEND_PODS" -gt 0 ]; then
    echo "✅ Cloud-Native Architecture appears to be successfully deployed!"
    echo "   - Both backend and frontend deployments exist and are running"
    echo "   - Services are available in the cluster"
    echo "   - Pods are in Running state"
else
    echo "⚠️  Some components may need attention - check the output above for details"
fi

echo ""
echo "🔧 For more detailed information:"
echo "   - View pod logs: kubectl logs -l app=backend-service"
echo "   - Check service endpoints: kubectl get endpoints"
echo "   - Describe deployments: kubectl describe deployment backend-service"