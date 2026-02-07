#!/bin/bash
# Verify monitoring and logging capabilities using kubectl-ai and Kagent

set -e

echo "=== Kubernetes Monitoring and Logging Verification ==="
echo ""

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster not accessible"
    exit 1
fi

echo "✓ Kubernetes cluster is accessible"
echo ""

# Function to run kubectl-ai or fallback to standard kubectl
run_kubectl_ai() {
    local query=$1
    local fallback_cmd=$2

    if command -v kubectl-ai &> /dev/null; then
        echo "Using kubectl-ai: $query"
        kubectl-ai "$query"
    else
        echo "kubectl-ai not available, using standard kubectl"
        eval "$fallback_cmd"
    fi
    echo ""
}

# 1. Check cluster health
echo "=== Cluster Health ==="
run_kubectl_ai "show cluster health" "kubectl get nodes && kubectl get componentstatuses 2>/dev/null || echo 'Component status not available'"

# 2. Check resource utilization
echo "=== Resource Utilization ==="
run_kubectl_ai "show resource usage for all pods" "kubectl top pods --all-namespaces 2>/dev/null || echo 'Metrics server not available. Install with: kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml'"

# 3. Check deployment status
echo "=== Deployment Status ==="
run_kubectl_ai "describe all deployments" "kubectl get deployments -o wide"

# 4. Check pod status and events
echo "=== Pod Status ==="
run_kubectl_ai "show all pods with their status" "kubectl get pods -o wide"

echo ""
echo "=== Recent Pod Events ==="
kubectl get events --sort-by='.lastTimestamp' | tail -20

# 5. Backend logs
echo ""
echo "=== Backend Logs (last 20 lines) ==="
run_kubectl_ai "show logs from backend pods" "kubectl logs -l app=todo-backend --tail=20"

# 6. Frontend logs
echo ""
echo "=== Frontend Logs (last 20 lines) ==="
run_kubectl_ai "show logs from frontend pods" "kubectl logs -l app=todo-frontend --tail=20"

# 7. Service endpoints
echo ""
echo "=== Service Endpoints ==="
run_kubectl_ai "show all service endpoints" "kubectl get endpoints"

# 8. Resource quotas and limits
echo ""
echo "=== Resource Limits ==="
kubectl describe deployment backend-deployment | grep -A 5 "Limits:"
kubectl describe deployment frontend-deployment | grep -A 5 "Limits:"

# 9. Health check status
echo ""
echo "=== Health Check Status ==="
echo "Backend health checks:"
kubectl describe deployment backend-deployment | grep -A 3 "Liveness:"
kubectl describe deployment backend-deployment | grep -A 3 "Readiness:"

echo ""
echo "Frontend health checks:"
kubectl describe deployment frontend-deployment | grep -A 3 "Liveness:"
kubectl describe deployment frontend-deployment | grep -A 3 "Readiness:"

# 10. Network policies (if any)
echo ""
echo "=== Network Policies ==="
kubectl get networkpolicies 2>/dev/null || echo "No network policies configured"

# 11. Persistent volumes (if any)
echo ""
echo "=== Persistent Volumes ==="
kubectl get pv,pvc 2>/dev/null || echo "No persistent volumes"

# 12. ConfigMaps and Secrets
echo ""
echo "=== ConfigMaps and Secrets ==="
kubectl get configmaps
kubectl get secrets

echo ""
echo "=== Monitoring Summary ==="
echo ""

# Count pods by status
RUNNING=$(kubectl get pods --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)
PENDING=$(kubectl get pods --field-selector=status.phase=Pending --no-headers 2>/dev/null | wc -l)
FAILED=$(kubectl get pods --field-selector=status.phase=Failed --no-headers 2>/dev/null | wc -l)

echo "Pod Status:"
echo "  Running: $RUNNING"
echo "  Pending: $PENDING"
echo "  Failed: $FAILED"

echo ""
echo "=== Verification Complete ==="
echo ""
echo "Useful monitoring commands:"
echo "  Watch pods: kubectl get pods -w"
echo "  Stream logs: kubectl logs -f -l app=todo-backend"
echo "  Port forward: kubectl port-forward svc/backend-service 8000:8000"
echo "  Describe issues: kubectl describe pod <pod-name>"
echo ""
echo "If kubectl-ai is installed:"
echo "  kubectl-ai 'show me pods with errors'"
echo "  kubectl-ai 'why is my deployment not ready'"
echo "  kubectl-ai 'show resource usage'"
