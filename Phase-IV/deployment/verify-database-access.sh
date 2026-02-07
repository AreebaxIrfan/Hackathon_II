#!/bin/bash
# Database Connectivity Verification Script
# Run this after Minikube cluster is started

echo "=== Neon Database Connectivity Verification ==="
echo ""

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster not accessible"
    echo "   Please start Minikube: minikube start"
    exit 1
fi

echo "✓ Kubernetes cluster is accessible"
echo ""

# Check if database secret exists
if kubectl get secret database-secret &> /dev/null; then
    echo "✓ Database secret exists"
else
    echo "⚠ Database secret not found"
    echo "   Create secret with: kubectl create secret generic database-secret --from-literal=DATABASE_URL=<your-neon-url>"
fi

echo ""
echo "=== Testing Database Connection ==="

# Create a test pod to verify database connectivity
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: db-test-pod
spec:
  containers:
  - name: postgres-client
    image: postgres:15-alpine
    command: ['sh', '-c', 'sleep 3600']
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: database-secret
          key: DATABASE_URL
          optional: true
  restartPolicy: Never
EOF

echo "⏳ Waiting for test pod to be ready..."
kubectl wait --for=condition=Ready pod/db-test-pod --timeout=60s

if [ $? -eq 0 ]; then
    echo "✓ Test pod is ready"
    echo ""
    echo "Testing database connection..."

    # Extract connection details and test
    kubectl exec db-test-pod -- sh -c 'if [ -n "$DATABASE_URL" ]; then echo "✓ DATABASE_URL is set"; else echo "❌ DATABASE_URL not set"; fi'

    echo ""
    echo "To test actual connectivity, run:"
    echo "kubectl exec -it db-test-pod -- psql \$DATABASE_URL -c 'SELECT 1;'"
else
    echo "❌ Test pod failed to start"
fi

echo ""
echo "Cleanup: kubectl delete pod db-test-pod"
