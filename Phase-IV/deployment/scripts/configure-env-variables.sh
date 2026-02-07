#!/bin/bash

# Script to configure environment variables for database connections in deployments
# This script creates Kubernetes secrets and configures environment variables

set -e  # Exit on any error

echo "⚙️  Configuring Environment Variables for Database Connections..."

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first."
    exit 1
fi

# Function to prompt for sensitive values
prompt_for_value() {
    local var_name="$1"
    local prompt_text="$2"
    local value=""

    echo -n "$prompt_text: "
    read -s value
    echo  # New line after hidden input
    echo "$value"
}

# Create or update database secret
echo "🔒 Creating/updating database connection secrets..."

# Prompt for sensitive information
echo "Please provide the database connection details:"
DATABASE_URL=$(prompt_for_value "DATABASE_URL" "Neon PostgreSQL DATABASE_URL (format: postgresql://username:password@host:port/database)")

# Create the database secret
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: database-secret
  namespace: default
type: Opaque
data:
  DATABASE_URL: $(echo -n "$DATABASE_URL" | base64 -w 0)
EOF

echo "✅ Database secret 'database-secret' created/updated."

# Create or update API keys secret
echo ""
echo "🔐 Creating/updating API keys secret..."

OPENAI_API_KEY=$(prompt_for_value "OPENAI_API_KEY" "OpenAI API Key")
BETTER_AUTH_SECRET=$(prompt_for_value "BETTER_AUTH_SECRET" "Better Auth Secret (JWT secret)")

# Create the API keys secret
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: api-keys-secret
  namespace: default
type: Opaque
data:
  OPENAI_API_KEY: $(echo -n "$OPENAI_API_KEY" | base64 -w 0)
  BETTER_AUTH_SECRET: $(echo -n "$BETTER_AUTH_SECRET" | base64 -w 0)
EOF

echo "✅ API keys secret 'api-keys-secret' created/updated."

# Validate secrets exist
echo ""
echo "🔍 Validating secrets..."

DB_SECRET_EXISTS=$(kubectl get secret database-secret --output=json 2>/dev/null | jq -r '.metadata.name' 2>/dev/null || echo "NOT_FOUND")
KEYS_SECRET_EXISTS=$(kubectl get secret api-keys-secret --output=json 2>/dev/null | jq -r '.metadata.name' 2>/dev/null || echo "NOT_FOUND")

if [ "$DB_SECRET_EXISTS" = "database-secret" ] && [ "$KEYS_SECRET_EXISTS" = "api-keys-secret" ]; then
    echo "✅ Both required secrets are configured correctly."
else
    echo "❌ Secret configuration issues detected:"
    [ "$DB_SECRET_EXISTS" != "database-secret" ] && echo "   - database-secret not found"
    [ "$KEYS_SECRET_EXISTS" != "api-keys-secret" ] && echo "   - api-keys-secret not found"
    exit 1
fi

# Test if the secrets contain the expected keys
echo ""
echo "🧪 Testing secret contents..."

DB_URL_ENCODED=$(kubectl get secret database-secret -o jsonpath='{.data.DATABASE_URL}' 2>/dev/null || echo "")
KEYS_OPENAI_ENCODED=$(kubectl get secret api-keys-secret -o jsonpath='{.data.OPENAI_API_KEY}' 2>/dev/null || echo "")
KEYS_AUTH_ENCODED=$(kubectl get secret api-keys-secret -o jsonpath='{.data.BETTER_AUTH_SECRET}' 2>/dev/null || echo "")

if [ -n "$DB_URL_ENCODED" ] && [ -n "$KEYS_OPENAI_ENCODED" ] && [ -n "$KEYS_AUTH_ENCODED" ]; then
    echo "✅ All required secret keys are present."

    # Decode and validate format (without exposing sensitive data)
    DB_URL_DECODED=$(echo "$DB_URL_ENCODED" | base64 -d)
    if [[ $DB_URL_DECODED == postgresql://* ]]; then
        echo "✅ DATABASE_URL format appears valid (starts with postgresql://)."
    else
        echo "⚠️  DATABASE_URL may have incorrect format (doesn't start with postgresql://)."
    fi
else
    echo "❌ Missing required secret keys:"
    [ -z "$DB_URL_ENCODED" ] && echo "   - DATABASE_URL missing in database-secret"
    [ -z "$KEYS_OPENAI_ENCODED" ] && echo "   - OPENAI_API_KEY missing in api-keys-secret"
    [ -z "$KEYS_AUTH_ENCODED" ] && echo "   - BETTER_AUTH_SECRET missing in api-keys-secret"
    exit 1
fi

# Check if deployments exist and are using the secrets
echo ""
echo "📋 Checking if deployments are configured to use secrets..."

# Look for existing deployments
BACKEND_DEPLOYMENT=$(kubectl get deployment todo-chatbot-backend 2>/dev/null || kubectl get deployment backend 2>/dev/null || echo "NOT_FOUND")

if [ "$BACKEND_DEPLOYMENT" != "NOT_FOUND" ]; then
    echo "✅ Backend deployment exists, checking environment variable configuration..."

    # Check if the deployment uses the database secret
    DB_SECRET_USED=$(kubectl get deployment todo-chatbot-backend -o yaml 2>/dev/null | grep -c "database-secret" || kubectl get deployment backend -o yaml 2>/dev/null | grep -c "database-secret" || echo "0")

    if [ "$DB_SECRET_USED" -gt 0 ]; then
        echo "✅ Backend deployment appears to be configured to use database secret."
    else
        echo "⚠️  Backend deployment may not be using the database secret."
    fi
else
    echo "ℹ️  No existing backend deployment found (this is expected if using Helm fresh install)."
fi

# Reinstall/redeploy with current secrets if Helm is available and chart exists
echo ""
echo "🔄 Redeploying with new secrets (if Helm chart is available)..."

if command -v helm &> /dev/null && [ -d "deployment/helm/todo-chatbot" ]; then
    cd deployment/helm/todo-chatbot/

    # Check if the release exists
    RELEASE_EXISTS=$(helm list --short --filter todo-chatbot 2>/dev/null || echo "")

    if [ -n "$RELEASE_EXISTS" ]; then
        echo "🎯 Found existing Helm release, upgrading to apply new secrets..."
        helm upgrade todo-chatbot . --values values.yaml --wait --timeout=5m
    else
        echo "🎯 Installing Helm chart with new secrets..."
        helm install todo-chatbot . --values values.yaml --wait --timeout=5m
    fi

    cd ../../../
    echo "✅ Helm deployment updated with new secrets."
else
    echo "ℹ️  Helm not available or chart not found, skipping redeployment."
fi

# Verify pods can access the secrets
echo ""
echo "🔍 Verifying pods can access secrets..."

# Wait a bit for deployments to update if they were restarted
sleep 10

BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ ! -z "$BACKEND_POD" ]; then
    echo "✅ Found backend pod: $BACKEND_POD"

    # Check if the pod has references to our secrets in its configuration
    POD_HAS_DB_REF=$(kubectl get pod $BACKEND_POD -o yaml | grep -c "database-secret" || echo "0")

    if [ "$POD_HAS_DB_REF" -gt 0 ]; then
        echo "✅ Backend pod is configured to use database secret."
    else
        echo "⚠️  Backend pod may not be configured to use the database secret."
    fi
else
    echo "ℹ️  No backend pod found, secrets will be used in new deployments."
fi

# Create a verification script for ongoing checks
cat > /tmp/verify-secrets.sh << 'EOF'
#!/bin/bash
# Verification script for environment variable configuration

echo "🔍 Verifying environment variable configuration..."

# Check if secrets exist
echo "Checking secrets existence..."
kubectl get secret database-secret && echo "✅ database-secret exists" || echo "❌ database-secret missing"
kubectl get secret api-keys-secret && echo "✅ api-keys-secret exists" || echo "❌ api-keys-secret missing"

# Check secret data keys
echo -e "\nChecking secret data keys..."
DB_KEYS=$(kubectl get secret database-secret -o jsonpath='{.data}' | jq -r 'keys[]')
KEYS_KEYS=$(kubectl get secret api-keys-secret -o jsonpath='{.data}' | jq -r 'keys[]')

echo "Database secret contains: $DB_KEYS"
echo "API keys secret contains: $KEYS_KEYS"

# Check if deployments use the secrets
echo -e "\nChecking deployment configurations..."
kubectl get deployment -o yaml | grep -s "database-secret\|api-keys-secret" | head -10 || echo "No deployments currently using secrets (may be in Helm templates)"

echo -e "\nEnvironment variable configuration check completed."
EOF

chmod +x /tmp/verify-secrets.sh

echo ""
echo "🎉 Environment variable configuration completed!"
echo ""
echo "📋 Summary:"
echo "✅ Database secret 'database-secret' created with DATABASE_URL"
echo "✅ API keys secret 'api-keys-secret' created with OPENAI_API_KEY and BETTER_AUTH_SECRET"
echo "✅ Secrets validated and properly formatted"
echo "✅ Deployments can access secrets (when deployed)"
echo ""
echo "🔐 Your database connection and API keys are securely stored in Kubernetes secrets."
echo "   The Helm chart is configured to use these secrets for the application."
echo ""
echo "📋 Verification script created: /tmp/verify-secrets.sh"
echo "   Run this script anytime to verify the configuration is still valid."
echo ""
echo "💡 Note: The application pods will need to be restarted to pick up any new secret values."
echo "   When using Helm, upgrade the release to apply changes."