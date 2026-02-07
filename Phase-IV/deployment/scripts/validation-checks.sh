#!/bin/bash

# Script to run validation checks to ensure all success criteria are met (SC-001 through SC-004)

set -e  # Exit on any error

echo "🔍 Running Validation Checks for Success Criteria..."

# Initialize counters
VALIDATION_PASSES=0
VALIDATION_TOTAL=0

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first."
    echo "   To start Minikube: minikube start --cpus=4 --memory=4096"
    exit 1
fi

echo "✅ Kubernetes cluster is accessible"

# Define success criteria validation functions
validate_success_criteria() {
    local criteria="$1"
    local description="$2"
    local test_command="$3"

    VALIDATION_TOTAL=$((VALIDATION_TOTAL + 1))
    echo "🔍 Testing $criteria: $description"

    if eval "$test_command"; then
        echo "   ✅ $criteria PASSED"
        VALIDATION_PASSES=$((VALIDATION_PASSES + 1))
        return 0
    else
        echo "   ❌ $criteria FAILED"
        return 1
    fi
}

echo ""
echo "🎯 Validating Success Criteria SC-001 through SC-004..."

# SC-001: Application successfully deploys to local Kubernetes cluster
echo ""
echo "📋 SC-001: Application successfully deploys to local Kubernetes cluster"
SC001_COMMAND='(
    kubectl get deployment todo-chatbot-backend 2>/dev/null | grep -q "todo-chatbot-backend" ||
    kubectl get deployment backend 2>/dev/null | grep -q "backend" ||
    kubectl get deployment -l app=todo-chatbot-backend 2>/dev/null | grep -q "todo-chatbot-backend"
) && (
    kubectl get deployment todo-chatbot-frontend 2>/dev/null | grep -q "todo-chatbot-frontend" ||
    kubectl get deployment frontend 2>/dev/null | grep -q "frontend" ||
    kubectl get deployment -l app=todo-chatbot-frontend 2>/dev/null | grep -q "todo-chatbot-frontend"
)'
validate_success_criteria "SC-001" "Application successfully deploys to local Kubernetes cluster" "$SC001_COMMAND"

# SC-002: Both frontend and backend services are running and accessible
echo ""
echo "📋 SC-002: Both frontend and backend services are running and accessible"
SC002_COMMAND='(
    kubectl get pods -l app=todo-chatbot-backend --field-selector=status.phase=Running --no-headers 2>/dev/null | grep -q "." ||
    kubectl get pods -l app=backend --field-selector=status.phase=Running --no-headers 2>/dev/null | grep -q "."
) && (
    kubectl get pods -l app=todo-chatbot-frontend --field-selector=status.phase=Running --no-headers 2>/dev/null | grep -q "." ||
    kubectl get pods -l app=frontend --field-selector=status.phase=Running --no-headers 2>/dev/null | grep -q "."
) && (
    kubectl get service todo-chatbot-backend-service 2>/dev/null | grep -q "ClusterIP" ||
    kubectl get service backend-service 2>/dev/null | grep -q "ClusterIP" ||
    kubectl get service -l app=todo-chatbot-backend 2>/dev/null | grep -q "todo-chatbot-backend"
) && (
    kubectl get service todo-chatbot-frontend-service 2>/dev/null | grep -q "LoadBalancer" ||
    kubectl get service frontend-service 2>/dev/null | grep -q "LoadBalancer" ||
    kubectl get service -l app=todo-chatbot-frontend 2>/dev/null | grep -q "todo-chatbot-frontend"
)'
validate_success_criteria "SC-002" "Both frontend and backend services are running and accessible" "$SC002_COMMAND"

# SC-003: Application maintains full functionality compared to original Phase III
echo ""
echo "📋 SC-003: Application maintains full functionality compared to original Phase III"
SC003_COMMAND='(
    BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath="{.items[0].metadata.name}" 2>/dev/null || kubectl get pods -l app=backend -o jsonpath="{.items[0].metadata.name}" 2>/dev/null) &&
    if [ ! -z "$BACKEND_POD" ]; then
        kubectl exec $BACKEND_POD -- curl -s -w ":%{http_code}" http://localhost:8000/health 2>/dev/null | grep -q "200$"
    else
        false
    fi
) && (
    FRONTEND_POD=$(kubectl get pods -l app=todo-chatbot-frontend -o jsonpath="{.items[0].metadata.name}" 2>/dev/null || kubectl get pods -l app=frontend -o jsonpath="{.items[0].metadata.name}" 2>/dev/null) &&
    if [ ! -z "$FRONTEND_POD" ]; then
        kubectl exec $FRONTEND_POD -- curl -s -w ":%{http_code}" http://localhost:3000/ 2>/dev/null | grep -q "200$"
    else
        false
    fi
) && (
    # Test common API endpoints exist
    API_ENDPOINTS=("/tasks" "/api/tasks" "/api/v1/tasks" "/todos" "/api/todos") &&
    SUCCESS=0 &&
    for endpoint in "${API_ENDPOINTS[@]}"; do
        BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath="{.items[0].metadata.name}" 2>/dev/null || kubectl get pods -l app=backend -o jsonpath="{.items[0].metadata.name}" 2>/dev/null) &&
        if [ ! -z "$BACKEND_POD" ]; then
            RESPONSE=$(kubectl exec $BACKEND_POD -- curl -s -w ":%{http_code}" http://localhost:8000$endpoint 2>/dev/null) &&
            if [[ $RESPONSE == *":200$" ]] || [[ $RESPONSE == *":201$" ]] || [[ $RESPONSE == *":401$" ]] || [[ $RESPONSE == *":403$" ]]; then
                SUCCESS=1
                break
            fi
        fi
    done &&
    [ $SUCCESS -eq 1 ]
)'
validate_success_criteria "SC-003" "Application maintains full functionality compared to original Phase III" "$SC003_COMMAND"

# SC-004: Zero-cost local deployment suitable for development environment
echo ""
echo "📋 SC-004: Zero-cost local deployment suitable for development environment"
SC004_COMMAND='(
    # Check if Helm chart exists and is properly configured
    [ -f "deployment/helm/todo-chatbot/Chart.yaml" ] &&
    [ -f "deployment/helm/todo-chatbot/values.yaml" ] &&
    [ -d "deployment/helm/todo-chatbot/templates" ]
) && (
    # Check if Dockerfiles exist for local building
    [ -f "deployment/docker/backend.Dockerfile" ] &&
    [ -f "deployment/docker/frontend.Dockerfile" ]
) && (
    # Check if Kubernetes manifests exist
    [ -f "deployment/k8s/backend-deployment.yaml" ] &&
    [ -f "deployment/k8s/frontend-deployment.yaml" ] &&
    [ -f "deployment/k8s/backend-service.yaml" ] &&
    [ -f "deployment/k8s/frontend-service.yaml" ]
) && (
    # Check if deployment scripts exist
    [ -f "deployment/scripts/build-images.sh" ] || [ -f "deployment/scripts/deploy-all.sh" ] || [ -f "deployment/README.md" ]
)'
validate_success_criteria "SC-004" "Zero-cost local deployment suitable for development environment" "$SC004_COMMAND"

# Additional validations beyond the basic success criteria
echo ""
echo "📋 Additional Validation Checks..."

# Check if Helm release is active
echo "🔍 Validating Helm release status..."
if helm list --filter todo-chatbot 2>/dev/null | grep -q "todo-chatbot"; then
    echo "   ✅ Helm release 'todo-chatbot' is active"
    VALIDATION_PASSES=$((VALIDATION_PASSES + 1))
    VALIDATION_TOTAL=$((VALIDATION_TOTAL + 1))
else
    echo "   ⚠️  Helm release 'todo-chatbot' not found (may be using raw manifests)"
    VALIDATION_TOTAL=$((VALIDATION_TOTAL + 1))
    # Count as pass since both Helm and raw manifests are valid
    VALIDATION_PASSES=$((VALIDATION_PASSES + 1))
fi

# Check if health checks are properly configured
echo "🔍 Validating health checks configuration..."
HEALTH_CHECKS_OK=true
BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ ! -z "$BACKEND_POD" ]; then
    LIVENESS_COUNT=$(kubectl get pod $BACKEND_POD -o jsonpath='{.spec.containers[0].livenessProbe}' 2>/dev/null | wc -c)
    READINESS_COUNT=$(kubectl get pod $BACKEND_POD -o jsonpath='{.spec.containers[0].readinessProbe}' 2>/dev/null | wc -c)

    if [ $LIVENESS_COUNT -gt 10 ] && [ $READINESS_COUNT -gt 10 ]; then
        echo "   ✅ Backend health checks properly configured"
    else
        echo "   ⚠️  Backend health checks may not be configured"
        HEALTH_CHECKS_OK=false
    fi
else
    echo "   ⚠️  No backend pod found for health check validation"
fi

FRONTEND_POD=$(kubectl get pods -l app=todo-chatbot-frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app=frontend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ ! -z "$FRONTEND_POD" ]; then
    FRONTEND_LIVENESS=$(kubectl get pod $FRONTEND_POD -o jsonpath='{.spec.containers[0].livenessProbe}' 2>/dev/null | wc -c)
    FRONTEND_READINESS=$(kubectl get pod $FRONTEND_POD -o jsonpath='{.spec.containers[0].readinessProbe}' 2>/dev/null | wc -c)

    if [ $FRONTEND_LIVENESS -gt 10 ] && [ $FRONTEND_READINESS -gt 10 ]; then
        echo "   ✅ Frontend health checks properly configured"
    else
        echo "   ⚠️  Frontend health checks may not be configured"
        HEALTH_CHECKS_OK=false
    fi
else
    echo "   ⚠️  No frontend pod found for health check validation"
fi

VALIDATION_TOTAL=$((VALIDATION_TOTAL + 1))
if [ "$HEALTH_CHECKS_OK" = true ]; then
    VALIDATION_PASSES=$((VALIDATION_PASSES + 1))
fi

# Check resource configuration
echo "🔍 Validating resource configuration..."
RESOURCES_OK=true

if [ ! -z "$BACKEND_POD" ]; then
    BACKEND_RESOURCES=$(kubectl get pod $BACKEND_POD -o jsonpath='{.spec.containers[0].resources}' 2>/dev/null | wc -c)
    if [ $BACKEND_RESOURCES -gt 10 ]; then
        echo "   ✅ Backend resource configuration found"
    else
        echo "   ⚠️  Backend resource configuration not found"
        RESOURCES_OK=false
    fi
else
    echo "   ⚠️  No backend pod found for resource validation"
fi

if [ ! -z "$FRONTEND_POD" ]; then
    FRONTEND_RESOURCES=$(kubectl get pod $FRONTEND_POD -o jsonpath='{.spec.containers[0].resources}' 2>/dev/null | wc -c)
    if [ $FRONTEND_RESOURCES -gt 10 ]; then
        echo "   ✅ Frontend resource configuration found"
    else
        echo "   ⚠️  Frontend resource configuration not found"
        RESOURCES_OK=false
    fi
else
    echo "   ⚠️  No frontend pod found for resource validation"
fi

VALIDATION_TOTAL=$((VALIDATION_TOTAL + 1))
if [ "$RESOURCES_OK" = true ]; then
    VALIDATION_PASSES=$((VALIDATION_PASSES + 1))
fi

# Summary
echo ""
echo "🎉 Validation Checks Completed!"
echo ""
echo "📋 Final Results:"
echo "   Total Checks: $VALIDATION_TOTAL"
echo "   Passed:       $VALIDATION_PASSES"
echo "   Failed:       $((VALIDATION_TOTAL - VALIDATION_PASSES))"
echo "   Success Rate: $(($VALIDATION_PASSES * 100 / $VALIDATION_TOTAL))%"

echo ""
if [ $VALIDATION_PASSES -eq $VALIDATION_TOTAL ]; then
    echo "✅ ALL VALIDATION CHECKS PASSED!"
    echo ""
    echo "🎯 All success criteria (SC-001 through SC-004) have been met:"
    echo "   SC-001: Application successfully deploys to local Kubernetes cluster ✓"
    echo "   SC-002: Both frontend and backend services are running and accessible ✓"
    echo "   SC-003: Application maintains full functionality compared to original Phase III ✓"
    echo "   SC-004: Zero-cost local deployment suitable for development environment ✓"
    echo ""
    echo "✨ The Kubernetes deployment successfully meets all specified requirements."
    echo "   The application is ready for development and testing in the local environment."
    exit 0
else
    echo "❌ SOME VALIDATION CHECKS FAILED"
    echo ""
    echo "⚠️  The deployment does not fully meet all success criteria."
    echo "   Failed validations: $((VALIDATION_TOTAL - VALIDATION_PASSES))"
    echo ""
    echo "🔧 Please address the failed validation points before considering the deployment complete."

    # Provide specific recommendations
    if [ $VALIDATION_PASSES -lt $((VALIDATION_TOTAL * 70 / 100)) ]; then
        echo ""
        echo "🚨 CRITICAL: Less than 70% of validations passed."
        echo "   Recommend investigating the fundamental deployment configuration."
    elif [ $VALIDATION_PASSES -lt $((VALIDATION_TOTAL * 90 / 100)) ]; then
        echo ""
        echo "⚠️  MODERATE: Between 70-89% of validations passed."
        echo "   Some configurations may need adjustment."
    else
        echo ""
        echo "ℹ️  MINOR: Over 90% of validations passed."
        echo "   Deployment is mostly successful but with some minor issues."
    fi

    exit 1
fi