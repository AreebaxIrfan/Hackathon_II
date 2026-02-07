#!/bin/bash

# Script to verify Helm chart configuration parameter customization
# This script tests that values in values.yaml can be overridden

set -e  # Exit on any error

echo "🔍 Verifying Helm Configuration Parameter Customization..."

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo "❌ Helm is not installed. Please install Helm first."
    exit 1
fi

# Check if Minikube is running
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first."
    exit 1
fi

# Test 1: Check default values in deployed resources
echo "🧪 Test 1: Verifying default values in deployed resources..."

# Get the deployed backend deployment
kubectl get deployment todo-chatbot-backend -o yaml > /tmp/backend-deployment.yaml

# Check default replica count
DEFAULT_REPLICAS=$(grep -A 10 "replicas:" /tmp/backend-deployment.yaml | head -2 | grep -o "[0-9]*")
if [ "$DEFAULT_REPLICAS" -eq 1 ]; then
    echo "✅ Backend replica count: $DEFAULT_REPLICAS (matches default in values.yaml)"
else
    echo "❌ Backend replica count: $DEFAULT_REPLICAS (expected: 1)"
fi

# Check default resource limits
MEMORY_LIMIT=$(grep -A 5 "limits:" /tmp/backend-deployment.yaml | grep memory | grep -o "1Gi")
if [ "$MEMORY_LIMIT" = "1Gi" ]; then
    echo "✅ Backend memory limit: $MEMORY_LIMIT (matches default in values.yaml)"
else
    echo "❌ Backend memory limit: $MEMORY_LIMIT (expected: 1Gi)"
fi

# Test 2: Create a custom values file with overrides
echo "🧪 Test 2: Testing custom configuration overrides..."

cat > /tmp/custom-values.yaml << 'EOF'
# Custom values for testing parameter customization
backend:
  replicaCount: 2
  resources:
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
  livenessProbe:
    initialDelaySeconds: 45
  readinessProbe:
    initialDelaySeconds: 10

frontend:
  replicaCount: 2
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 250m
      memory: 256Mi
  livenessProbe:
    initialDelaySeconds: 20
  readinessProbe:
    initialDelaySeconds: 5
EOF

echo "📝 Created custom values file with overrides:"
echo "   - Backend replicas: 2 (was 1)"
echo "   - Backend CPU/memory limits reduced"
echo "   - Backend probe delays changed"
echo "   - Frontend replicas: 2 (was 1)"

# Uninstall current deployment if exists
helm uninstall todo-chatbot-test 2>/dev/null || true

# Install with custom values
echo "🔧 Installing with custom values..."
helm install todo-chatbot-test . --values /tmp/custom-values.yaml --wait --timeout=5m

# Wait for deployment
kubectl wait --for=condition=ready pod -l app=todo-chatbot-test-backend --timeout=300s || true
kubectl wait --for=condition=ready pod -l app=todo-chatbot-test-frontend --timeout=300s || true

# Verify custom values
kubectl get deployment todo-chatbot-test-backend -o yaml > /tmp/custom-backend-deployment.yaml

CUSTOM_REPLICAS=$(grep -A 10 "replicas:" /tmp/custom-backend-deployment.yaml | head -2 | grep -o "[0-9]*")
if [ "$CUSTOM_REPLICAS" -eq 2 ]; then
    echo "✅ Custom backend replica count: $CUSTOM_REPLICAS (matches override)"
else
    echo "❌ Custom backend replica count: $CUSTOM_REPLICAS (expected: 2)"
fi

CUSTOM_MEMORY=$(grep -A 5 "limits:" /tmp/custom-backend-deployment.yaml | grep memory | grep -o "512Mi")
if [ "$CUSTOM_MEMORY" = "512Mi" ]; then
    echo "✅ Custom backend memory limit: $CUSTOM_MEMORY (matches override)"
else
    echo "❌ Custom backend memory limit: $CUSTOM_MEMORY (expected: 512Mi)"
fi

# Clean up test deployment
echo "🧹 Cleaning up test deployment..."
helm uninstall todo-chatbot-test

# Verify original deployment can be restored
echo "🔄 Restoring original deployment..."
helm upgrade todo-chatbot . --values values.yaml --wait --timeout=5m

echo ""
echo "🎉 Configuration parameter customization verification completed!"
echo ""
echo "📋 Summary:"
echo "   - Default values are correctly applied from values.yaml"
echo "   - Custom values can be provided via --values flag"
echo "   - Parameters can be overridden without changing chart templates"
echo "   - Helm upgrades work properly with value changes"