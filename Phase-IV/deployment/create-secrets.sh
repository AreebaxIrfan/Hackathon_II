#!/bin/bash
# Create Kubernetes secrets for Todo Chatbot deployment
# This script creates template secrets - you must update with actual values

set -e

echo "=== Creating Kubernetes Secrets ==="
echo ""

# Check if kubectl is configured
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster not accessible"
    echo "   Please start Minikube: minikube start"
    exit 1
fi

echo "✓ Kubernetes cluster is accessible"
echo ""

# Prompt for database URL
echo "Enter your Neon PostgreSQL DATABASE_URL:"
read -s DATABASE_URL

if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL cannot be empty"
    exit 1
fi

# Prompt for OpenAI API key
echo ""
echo "Enter your OPENAI_API_KEY:"
read -s OPENAI_API_KEY

if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY cannot be empty"
    exit 1
fi

# Prompt for Better Auth secret
echo ""
echo "Enter your BETTER_AUTH_SECRET:"
read -s BETTER_AUTH_SECRET

if [ -z "$BETTER_AUTH_SECRET" ]; then
    echo "❌ BETTER_AUTH_SECRET cannot be empty"
    exit 1
fi

echo ""
echo "Creating secrets..."

# Create database secret
kubectl create secret generic database-secret \
    --from-literal=DATABASE_URL="$DATABASE_URL" \
    --dry-run=client -o yaml | kubectl apply -f -

if [ $? -eq 0 ]; then
    echo "✓ database-secret created/updated"
else
    echo "❌ Failed to create database-secret"
    exit 1
fi

# Create API keys secret
kubectl create secret generic api-keys-secret \
    --from-literal=OPENAI_API_KEY="$OPENAI_API_KEY" \
    --from-literal=BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
    --dry-run=client -o yaml | kubectl apply -f -

if [ $? -eq 0 ]; then
    echo "✓ api-keys-secret created/updated"
else
    echo "❌ Failed to create api-keys-secret"
    exit 1
fi

echo ""
echo "=== Secrets Created Successfully ==="
echo ""
echo "Verify secrets:"
echo "kubectl get secrets"
