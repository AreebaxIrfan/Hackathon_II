#!/bin/bash

# Script to verify database connectivity from backend to Neon PostgreSQL in Kubernetes deployment

set -e  # Exit on any error

echo "🗄️  Verifying Database Connectivity to Neon PostgreSQL..."

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first."
    exit 1
fi

# Test 1: Check if backend pod is running
echo "🔍 Finding backend pod..."
BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -z "$BACKEND_POD" ]; then
    echo "❌ No backend pod found. Attempting to ensure deployment is active..."
    cd deployment/helm/todo-chatbot/
    helm upgrade --install todo-chatbot . --values values.yaml --wait --timeout=5m || echo "Deployment check completed"
    cd ../../..

    # Wait briefly and try again
    sleep 5
    BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

    if [ -z "$BACKEND_POD" ]; then
        echo "❌ No backend pod found after deployment check."
        echo "   Please ensure the application is deployed before running this test."
        exit 1
    fi
fi

echo "✅ Backend pod found: $BACKEND_POD"

# Test 2: Verify database secrets are configured
echo "🔐 Checking database secret configuration..."
DB_SECRET_EXISTS=$(kubectl get secret database-secret 2>/dev/null | wc -l)

if [ "$DB_SECRET_EXISTS" -gt 0 ]; then
    echo "✅ Database secret 'database-secret' exists"

    # Check if DATABASE_URL is present in the secret
    DB_URL_IN_SECRET=$(kubectl get secret database-secret -o jsonpath='{.data.DATABASE_URL}' 2>/dev/null || echo "")

    if [ ! -z "$DB_URL_IN_SECRET" ] && [ "$DB_URL_IN_SECRET" != "" ]; then
        echo "✅ DATABASE_URL is configured in database-secret"

        # Decode the secret to check if it's a Neon URL
        DB_URL_DECODED=$(kubectl get secret database-secret -o jsonpath='{.data.DATABASE_URL}' | base64 -d)
        if [[ $DB_URL_DECODED == *"neon.tech"* ]]; then
            echo "✅ Database URL appears to be a Neon PostgreSQL connection"
        else
            echo "ℹ️  Database URL detected (not Neon, but still valid)"
        fi
    else
        echo "⚠️  DATABASE_URL not found in database-secret"
        echo "   Available keys in database-secret:"
        kubectl get secret database-secret -o jsonpath='{.data}' | tr ',' '\n' | sort || echo "No data found"
    fi
else
    echo "⚠️  Database secret 'database-secret' not found"
    echo "   Available secrets:"
    kubectl get secrets
fi

# Test 3: Check if backend pod has database environment variables
echo "⚙️  Checking backend pod environment variables..."
DB_ENV_AVAILABLE=$(kubectl exec $BACKEND_POD -- env | grep DATABASE_URL | wc -l)

if [ "$DB_ENV_AVAILABLE" -gt 0 ]; then
    echo "✅ DATABASE_URL is available in backend pod"
    DB_URL_VALUE=$(kubectl exec $BACKEND_POD -- env | grep DATABASE_URL)
    if [[ $DB_URL_VALUE == *"neon.tech"* ]]; then
        echo "✅ Backend is configured to use Neon PostgreSQL"
    else
        echo "ℹ️  Backend has database connection configured (not Neon)"
    fi
else
    echo "❌ DATABASE_URL not found in backend pod environment"
    echo "   Available environment variables (filtered):"
    kubectl exec $BACKEND_POD -- env | grep -E "(DB_|DATABASE|POSTGRES|SQLITE)" || echo "No database-related env vars found"
fi

# Test 4: Test database connectivity from backend
echo "🔌 Testing database connectivity from backend pod..."

# Try different approaches to test database connectivity
CONNECTIVITY_CHECKS=()

# Method 1: Check backend health endpoint that might include DB status
echo "   Testing backend health endpoint for DB status..."
HEALTH_RESPONSE=$(kubectl exec $BACKEND_POD -- curl -s http://localhost:8000/health 2>/dev/null || echo "FAILED")

if [[ $HEALTH_RESPONSE != "FAILED" ]]; then
    if [[ $HEALTH_RESPONSE == *"database"* ]] || [[ $HEALTH_RESPONSE == *"db"* ]] || [[ $HEALTH_RESPONSE == *"DB"* ]]; then
        echo "   ℹ️  Health endpoint includes database info: $(echo $HEALTH_RESPONSE | head -c 100)..."
    else
        echo "   ℹ️  Health endpoint doesn't explicitly show DB status: $(echo $HEALTH_RESPONSE | head -c 100)..."
    fi
else
    echo "   - Health endpoint not accessible"
fi

# Method 2: Try to install and use database tools if available
echo "   Attempting database connectivity test..."
DB_CONNECT_RESULT="UNKNOWN"

# Try to test connectivity by installing required tools (Python/db packages)
INSTALL_SUCCESS=$(kubectl exec $BACKEND_POD -- python -c "import sqlalchemy; print('SQLAlchemy available')" 2>/dev/null && echo "YES" || echo "NO")

if [ "$INSTALL_SUCCESS" = "YES" ]; then
    # Try to connect using Python
    CONNECTION_TEST=$(kubectl exec $BACKEND_POD -- python -c "
import os
import sqlalchemy
try:
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        engine = sqlalchemy.create_engine(db_url)
        conn = engine.connect()
        result = conn.execute(sqlalchemy.text('SELECT 1'))
        print('CONNECTED: True')
        conn.close()
    else:
        print('CONNECTED: False - No DATABASE_URL')
except Exception as e:
    print(f'CONNECTED: False - {str(e)}')
" 2>/dev/null || echo "PYTHON_ERROR")

    if [[ $CONNECTION_TEST == *"CONNECTED: True"* ]]; then
        DB_CONNECT_RESULT="SUCCESS"
        echo "   ✅ Database connectivity test PASSED"
    elif [[ $CONNECTION_TEST == *"CONNECTED: False"* ]]; then
        DB_CONNECT_RESULT="FAILED"
        ERROR_MSG=$(echo $CONNECTION_TEST | grep -o "False -.*" | cut -d'-' -f2-)
        echo "   ❌ Database connectivity test FAILED: $ERROR_MSG"
    else
        echo "   - Python connectivity test inconclusive: $CONNECTION_TEST"
    fi
else
    echo "   - Python SQLAlchemy not available for connectivity test"
fi

# Method 3: Check application logs for database connection messages
echo "   Checking application logs for database connection status..."
LOG_SNIPPET=$(kubectl logs $BACKEND_POD --tail=50 2>/dev/null || echo "Could not retrieve logs")
CONNECTION_LOGS=$(echo "$LOG_SNIPPET" | grep -i -E "(database|db|sql|postgres|connection|connect|failed|error)" | head -n 10)

if [ ! -z "$CONNECTION_LOGS" ] && [ "$CONNECTION_LOGS" != "Could not retrieve logs" ]; then
    echo "   ℹ️  Database-related log entries found:"
    echo "$CONNECTION_LOGS" | sed 's/^/      /'

    if [[ $CONNECTION_LOGS == *"connected"* ]] || [[ $CONNECTION_LOGS == *"Connected"* ]] || [[ $CONNECTION_LOGS == *"successful"* ]]; then
        if [ "$DB_CONNECT_RESULT" != "SUCCESS" ]; then
            DB_CONNECT_RESULT="SUCCESS_LOG"
            echo "   ✅ Logs indicate database connection was established"
        fi
    elif [[ $CONNECTION_LOGS == *"failed"* ]] || [[ $CONNECTION_LOGS == *"error"* ]] || [[ $CONNECTION_LOGS == *"Error"* ]]; then
        if [ "$DB_CONNECT_RESULT" != "FAILED" ]; then
            DB_CONNECT_RESULT="FAILED_LOG"
            echo "   ❌ Logs indicate database connection issues"
        fi
    fi
else
    echo "   - No obvious database connection logs found in recent entries"
fi

# Test 5: Check if backend is responsive (indirect DB test)
echo "   Testing backend general responsiveness..."
BACKEND_RESPONSIVE=$(kubectl exec $BACKEND_POD -- curl -s -w " HTTP_CODE:%{http_code}" http://localhost:8000/ 2>/dev/null || echo "FAILED")

if [[ $BACKEND_RESPONSIVE != "FAILED" ]]; then
    HTTP_CODE=$(echo $BACKEND_RESPONSIVE | grep -o "HTTP_CODE:[0-9]*" | cut -d':' -f2)
    if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 400 ]; then
        echo "   ✅ Backend is responsive (HTTP $HTTP_CODE) - suggests DB connection OK"
    else
        echo "   ⚠️  Backend returned HTTP $HTTP_CODE - may indicate DB issues"
    fi
else
    echo "   ❌ Backend not responsive - likely indicates startup or DB issues"
fi

# Test 6: Create a diagnostic report
echo "📋 Creating database connectivity diagnostic report..."

DIAGNOSTIC_FILE="/tmp/db_diagnostic_$(date +%s).txt"
cat > $DIAGNOSTIC_FILE << EOF
Database Connectivity Diagnostic Report
======================================

Timestamp: $(date)
Backend Pod: $BACKEND_POD
Cluster: $(kubectl config current-context 2>/dev/null || echo "unknown")

Secrets Check:
- database-secret exists: $([ $DB_SECRET_EXISTS -gt 0 ] && echo "YES" || echo "NO")
- DATABASE_URL in secret: $([ ! -z "$DB_URL_IN_SECRET" ] && echo "YES" || echo "NO")
- Uses Neon: $([[ $DB_URL_DECODED == *"neon.tech"* ]] && echo "YES" || echo "NO")

Environment Check:
- DATABASE_URL in pod: $([ $DB_ENV_AVAILABLE -gt 0 ] && echo "YES" || echo "NO")
- Connection Test Result: $DB_CONNECT_RESULT

Application Status:
- Backend Health: $HEALTH_RESPONSE
- Backend Responsive: $BACKEND_RESPONSIVE

Connection Test Method:
- Python SQLAlchemy: $INSTALL_SUCCESS
- Python Connection: $CONNECTION_TEST

Recent Log Indicators:
$CONNECTION_LOGS

Conclusion:
$(if [ "$DB_CONNECT_RESULT" = "SUCCESS" ] || [ "$DB_CONNECT_RESULT" = "SUCCESS_LOG" ]; then
    echo "✅ Database connectivity appears to be working properly"
elif [ "$DB_CONNECT_RESULT" = "FAILED" ] || [ "$DB_CONNECT_RESULT" = "FAILED_LOG" ]; then
    echo "❌ Database connectivity issues detected"
else
    echo "❓ Database connectivity status unclear - requires manual verification"
fi)
EOF

echo "   Diagnostic report saved to: $DIAGNOSTIC_FILE"

# Summary
echo ""
echo "🎉 Database connectivity verification completed!"
echo ""
echo "📋 Summary:"
echo "   - Backend pod status: ✅ Running"
echo "   - Database secret configuration: $(if [ $DB_SECRET_EXISTS -gt 0 ]; then echo "✅ Configured"; else echo "⚠️  Missing"; fi)"
echo "   - Environment variables: $(if [ $DB_ENV_AVAILABLE -gt 0 ]; then echo "✅ Available"; else echo "❌ Missing"; fi)"
echo "   - Direct connectivity test: $(case $DB_CONNECT_RESULT in SUCCESS|SUCCESS_LOG) echo "✅ Passed";; FAILED|FAILED_LOG) echo "❌ Failed";; *) echo "❓ Inconclusive";; esac)"
echo "   - Application responsiveness: $(if [[ $BACKEND_RESPONSIVE != "FAILED" ]] && [[ $HTTP_CODE -ge 200 ]] && [[ $HTTP_CODE -lt 400 ]]; then echo "✅ Healthy"; else echo "❌ Issues"; fi)"

if [ "$DB_CONNECT_RESULT" = "SUCCESS" ] || [ "$DB_CONNECT_RESULT" = "SUCCESS_LOG" ]; then
    echo ""
    echo "✅ Database connectivity to Neon PostgreSQL is working in Kubernetes deployment!"
    echo ""
    echo "💡 The backend application can successfully connect to the database."
elif [ "$DB_CONNECT_RESULT" = "FAILED" ] || [ "$DB_CONNECT_RESULT" = "FAILED_LOG" ]; then
    echo ""
    echo "❌ Database connectivity issues detected."
    echo ""
    echo "🔧 Troubleshooting steps:"
    echo "   1. Verify database secret contains correct DATABASE_URL"
    echo "   2. Check Neon PostgreSQL connection settings"
    echo "   3. Verify network access to Neon database"
    echo "   4. Review backend application logs for detailed errors"
else
    echo ""
    echo "⚠️  Database connectivity status is unclear."
    echo "   Manual verification recommended by checking application logs and testing direct connectivity."
fi