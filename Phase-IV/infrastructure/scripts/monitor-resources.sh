#!/bin/bash

# Script to monitor cloud-native architecture resources
# This script demonstrates AI-assisted monitoring capabilities with kubectl-ai

set -e  # Exit on any error

echo "👁️  Monitoring Cloud-Native Architecture Resources..."

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

# Check for AI-assisted tools
if command_exists kubectl-ai; then
    echo "🤖 kubectl-ai found! Using AI-assisted monitoring commands..."
    USE_KCTL_AI=true
else
    echo "⚠️  kubectl-ai not found. Using standard kubectl commands..."
    USE_KCTL_AI=false
fi

if command_exists kagent; then
    echo "🤖 Kagent found! Available for advanced monitoring..."
    USE_KAGENT=true
else
    echo "⚠️  Kagent not found. Advanced AI monitoring not available."
    USE_KAGENT=false
fi

echo ""
echo "📊 Resource Monitoring Dashboard"
echo "================================"

# Get deployment status
echo ""
echo "📋 Deployment Status:"
if [ "$USE_KCTL_AI" = true ]; then
    kubectl-ai get deployments
else
    kubectl get deployments
fi

# Get service status
echo ""
echo "📡 Service Status:"
if [ "$USE_KCTL_AI" = true ]; then
    kubectl-ai get services
else
    kubectl get services
fi

# Get pod status
echo ""
echo "📦 Pod Status:"
if [ "$USE_KCTL_AI" = true ]; then
    kubectl-ai get pods -o wide
else
    kubectl get pods -o wide
fi

# Get resource usage if metrics server is available
echo ""
echo "📈 Resource Usage:"
if command_exists kubectl && kubectl top nodes &> /dev/null; then
    echo "Node Resources:"
    kubectl top nodes

    echo ""
    echo "Pod Resources:"
    kubectl top pods
else
    echo "⚠️  Metrics server not available. Install metrics server for resource monitoring:"
    echo "   minikube addons enable metrics-server"
    echo "   Or: kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"
fi

# Check logs for recent activity
echo ""
echo "📝 Recent Log Activity:"

# Get backend logs
BACKEND_POD=$(kubectl get pods -l app=$(kubectl get deployment | grep -E "(backend-service|.*-backend)" | head -1 | awk '{print $1}') -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -n "$BACKEND_POD" ]; then
    echo "Backend Pod ($BACKEND_POD) - Last 10 lines:"
    kubectl logs "$BACKEND_POD" --tail=10 2>/dev/null || echo "   (No logs available or error retrieving logs)"
else
    echo "No backend pod found for log inspection"
fi

# Get frontend logs
FRONTEND_POD=$(kubectl get pods -l app=$(kubectl get deployment | grep -E "(frontend-service|.*-frontend)" | head -1 | awk '{print $1}') -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -n "$FRONTEND_POD" ]; then
    echo "Frontend Pod ($FRONTEND_POD) - Last 10 lines:"
    kubectl logs "$FRONTEND_POD" --tail=10 2>/dev/null || echo "   (No logs available or error retrieving logs)"
else
    echo "No frontend pod found for log inspection"
fi

# Check events for any issues
echo ""
echo "🚨 Recent Events (errors/warnings):"
kubectl get events --sort-by='.lastTimestamp' --field-selector type!=Normal | tail -10

# Health check summary
echo ""
echo "🏥 Health Status Summary:"

# Check deployment readiness
BACKEND_DEPLOYMENT=$(kubectl get deployment | grep -E "(backend-service|.*-backend)" | head -1 | awk '{print $1}')
FRONTEND_DEPLOYMENT=$(kubectl get deployment | grep -E "(frontend-service|.*-frontend)" | head -1 | awk '{print $1}')

if [ -n "$BACKEND_DEPLOYMENT" ]; then
    READY_REPLICAS=$(kubectl get deployment "$BACKEND_DEPLOYMENT" -o jsonpath='{.status.readyReplicas}')
    DESIRED_REPLICAS=$(kubectl get deployment "$BACKEND_DEPLOYMENT" -o jsonpath='{.spec.replicas}')
    if [ "$READY_REPLICAS" -eq "$DESIRED_REPLICAS" ] && [ "$READY_REPLICAS" -gt 0 ]; then
        echo "✅ $BACKEND_DEPLOYMENT: $READY_REPLICAS/$DESIRED_REPLICAS replicas ready"
    else
        echo "❌ $BACKEND_DEPLOYMENT: $READY_REPLICAS/$DESIRED_REPLICAS replicas ready"
    fi
fi

if [ -n "$FRONTEND_DEPLOYMENT" ]; then
    READY_REPLICAS=$(kubectl get deployment "$FRONTEND_DEPLOYMENT" -o jsonpath='{.status.readyReplicas}')
    DESIRED_REPLICAS=$(kubectl get deployment "$FRONTEND_DEPLOYMENT" -o jsonpath='{.spec.replicas}')
    if [ "$READY_REPLICAS" -eq "$DESIRED_REPLICAS" ] && [ "$READY_REPLICAS" -gt 0 ]; then
        echo "✅ $FRONTEND_DEPLOYMENT: $READY_REPLICAS/$DESIRED_REPLICAS replicas ready"
    else
        echo "❌ $FRONTEND_DEPLOYMENT: $READY_REPLICAS/$DESIRED_REPLICAS replicas ready"
    fi
fi

# Show any resource constraints
echo ""
echo "⚠️  Resource Constraints Check:"
kubectl describe nodes | grep -E "(Insufficient|Evicted|Terminated)" | head -10 || echo "No immediate resource constraint issues found"

# If Kagent is available, show AI-powered insights
if [ "$USE_KAGENT" = true ]; then
    echo ""
    echo "🤖 AI Insights (via Kagent):"
    echo "Note: Kagent can provide advanced monitoring and optimization suggestions"
    echo "Run: kagent diagnose --component=kubernetes --type=monitoring"
    echo "Or: kagent analyze resources --duration=5m"
fi

echo ""
echo "🎯 Monitoring Summary:"
echo "   - Checked deployment, service, and pod status"
echo "   - Reviewed resource usage and capacity"
echo "   - Inspected logs and recent events"
echo "   - Verified readiness and health indicators"
echo ""
echo "💡 Tips for ongoing monitoring:"
echo "   - Set up Prometheus/Grafana for continuous monitoring"
echo "   - Configure alerting for critical metrics"
echo "   - Implement distributed tracing for service communication"
echo "   - Use KEDA for event-driven autoscaling"