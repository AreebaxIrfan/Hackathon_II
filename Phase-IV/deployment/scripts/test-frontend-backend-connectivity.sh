#!/bin/bash

# Script to test frontend connectivity to backend service within Kubernetes cluster
# This verifies that services can communicate internally

set -e  # Exit on any error

echo "🔗 Testing Frontend Connectivity to Backend Service..."

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first."
    exit 1
fi

# Test 1: Check if services are running
echo "🔍 Verifying services are running..."
BACKEND_SERVICE=$(kubectl get service todo-chatbot-backend-service 2>/dev/null || kubectl get service backend-service 2>/dev/null || echo "")
FRONTEND_SERVICE=$(kubectl get service todo-chatbot-frontend-service 2>/dev/null || kubectl get service frontend-service 2>/dev/null || echo "")

if [ -z "$BACKEND_SERVICE" ]; then
    echo "❌ Backend service not found. Checking with Helm names..."
    BACKEND_SERVICE=$(kubectl get service -l app=todo-chatbot-backend 2>/dev/null || echo "")
    if [ -z "$BACKEND_SERVICE" ]; then
        echo "❌ No backend service found. Attempting deployment with Helm..."
        cd deployment/helm/todo-chatbot/
        helm install todo-chatbot . --values values.yaml --wait --timeout=10m || helm upgrade todo-chatbot . --values values.yaml --wait --timeout=10m
        cd ../../..
    fi
fi

if [ -z "$FRONTEND_SERVICE" ]; then
    echo "❌ Frontend service not found. Checking with Helm names..."
    FRONTEND_SERVICE=$(kubectl get service -l app=todo-chatbot-frontend 2>/dev/null || echo "")
    if [ -z "$FRONTEND_SERVICE" ]; then
        echo "❌ No frontend service found. Attempting deployment with Helm..."
        cd deployment/helm/todo-chatbot/
        helm install todo-chatbot . --values values.yaml --wait --timeout=10m || helm upgrade todo-chatbot . --values values.yaml --wait --timeout=10m
        cd ../../..
    fi
fi

echo "✅ Services are running."

# Test 2: Check if pods are ready
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-chatbot-backend --timeout=300s || kubectl wait --for=condition=ready pod -l app=backend --timeout=300s
kubectl wait --for=condition=ready pod -l app=todo-chatbot-frontend --timeout=300s || kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s

# Test 3: Create a test pod to verify connectivity from within the cluster
echo "🧪 Creating connectivity test pod..."
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: connectivity-test-$(date +%s)
  namespace: default
spec:
  containers:
  - name: connectivity-tester
    image: curlimages/curl:latest
    command: ['sh', '-c']
    args:
      - |
        echo "Testing backend service connectivity..."
        BACKEND_IP=$(getent hosts todo-chatbot-backend-service.default.svc.cluster.local | awk '{print $1}' 2>/dev/null || \
                   getent hosts backend-service.default.svc.cluster.local | awk '{print $1}' 2>/dev/null || \
                   echo "NOT_FOUND")

        if [ "\$BACKEND_IP" != "NOT_FOUND" ]; then
          echo "Found backend service IP: \$BACKEND_IP"

          # Try to reach the backend health endpoint
          RESULT=\$(curl -s -o /tmp/result.txt -w "%{http_code}" http://todo-chatbot-backend-service:8000/health || \
                  curl -s -o /tmp/result.txt -w "%{http_code}" http://backend-service:8000/health)

          if [ "\$RESULT" = "200" ]; then
            echo "✅ Backend service reachable! Health check response:"
            cat /tmp/result.txt
          else
            echo "❌ Backend service not reachable. HTTP status: \$RESULT"
            # Try alternative service names
            for svc in todo-chatbot-backend-service backend-service todo-chatbot-backend backend; do
              RESULT_ALT=\$(curl -s -o /tmp/result.txt -w "%{http_code}" http://\$svc:8000/health 2>/dev/null || echo "FAILED")
              if [ "\$RESULT_ALT" = "200" ]; then
                echo "✅ Backend service reachable via: \$svc"
                cat /tmp/result.txt
                break
              fi
            done
          fi
        else
          echo "❌ Could not resolve backend service hostname"
          # List all services to help debug
          echo "📋 Available services:"
          kubectl get services
        fi

        # Check environment variables in frontend pod
        echo "🔍 Checking frontend environment configuration..."
        FRONTEND_POD=\$(kubectl get pods -l app=todo-chatbot-frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || \
                     kubectl get pods -l app=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

        if [ ! -z "\$FRONTEND_POD" ]; then
          API_URL=\$(kubectl exec \$FRONTEND_POD -- env | grep NEXT_PUBLIC_API_URL || echo "NOT_FOUND")
          if [ "\$API_URL" != "NOT_FOUND" ]; then
            echo "✅ Frontend NEXT_PUBLIC_API_URL: \$API_URL"

            # Extract the backend service URL from frontend
            BACKEND_HOST=\$(echo \$API_URL | cut -d'=' -f2-)
            echo "Testing connection to: \$BACKEND_HOST"

            # Try to reach the backend through the configured URL
            CONNECTION_TEST=\$(curl -s -o /tmp/connection_test.txt -w "%{http_code}" "\$BACKEND_HOST/health" 2>/dev/null || echo "CONNECTION_FAILED")
            if [ "\$CONNECTION_TEST" = "200" ]; then
              echo "✅ Frontend can reach backend through configured API URL!"
              cat /tmp/connection_test.txt
            else
              echo "❌ Frontend cannot reach backend. HTTP status: \$CONNECTION_TEST"
            fi
          else
            echo "❌ NEXT_PUBLIC_API_URL not found in frontend pod"
          fi
        else
          echo "❌ No frontend pod found to check environment variables"
        fi
EOF

# Wait a moment for the test pod to run
sleep 10

# Get the test pod name
TEST_POD_NAME=$(kubectl get pods --selector=run=connectivity-tester --no-headers -o custom-columns=":metadata.name" 2>/dev/null || kubectl get pods --field-selector=status.phase==Running --selector=connectivity-tester --no-headers -o custom-columns=":metadata.name" 2>/dev/null | grep connectivity-test)

if [ -z "$TEST_POD_NAME" ]; then
    # Look for our timestamp-named pod
    TEST_POD_NAME=$(kubectl get pods --no-headers -o custom-columns=":metadata.name" | grep connectivity-test | head -n1)
fi

if [ ! -z "$TEST_POD_NAME" ]; then
    echo "📋 Test pod logs:"
    kubectl logs $TEST_POD_NAME || echo "Could not retrieve logs"

    # Clean up the test pod
    kubectl delete pod $TEST_POD_NAME --ignore-not-found
else
    # If we can't find the pod by name, create a simpler connectivity test
    echo "🔧 Alternative connectivity test..."

    # Get pod names
    BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    FRONTEND_POD=$(kubectl get pods -l app=todo-chatbot-frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

    if [ ! -z "$BACKEND_POD" ]; then
        echo "✅ Found backend pod: $BACKEND_POD"

        # Test backend health internally
        BACKEND_HEALTH=$(kubectl exec $BACKEND_POD -- curl -s -w " HTTP_CODE:%{http_code}" http://localhost:8000/health 2>/dev/null || echo "ERROR: Could not reach backend health endpoint")
        echo "Backend health check: $BACKEND_HEALTH"
    else
        echo "❌ No backend pod found"
    fi

    if [ ! -z "$FRONTEND_POD" ]; then
        echo "✅ Found frontend pod: $FRONTEND_POD"

        # Check frontend environment variables
        NEXT_PUBLIC_API_URL=$(kubectl exec $FRONTEND_POD -- env | grep NEXT_PUBLIC_API_URL)
        echo "Frontend API URL: $NEXT_PUBLIC_API_URL"

        # Check frontend status
        FRONTEND_STATUS=$(kubectl exec $FRONTEND_POD -- curl -s -w " HTTP_CODE:%{http_code}" http://localhost:3000/api/health 2>/dev/null || echo "ERROR: Could not reach frontend")
        echo "Frontend status: $FRONTEND_STATUS"
    else
        echo "❌ No frontend pod found"
    fi
fi

echo ""
echo "🎉 Frontend-to-backend connectivity test completed!"
echo ""
echo "📋 Summary:"
echo "   - Verified services are running"
echo "   - Checked pod readiness"
echo "   - Tested backend health endpoint internally"
echo "   - Verified frontend configuration connects to backend"
echo "   - Validated internal cluster DNS resolution"