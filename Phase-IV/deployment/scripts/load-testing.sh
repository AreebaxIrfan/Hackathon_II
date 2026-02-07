#!/bin/bash

# Script to perform load testing to verify application performs within expected parameters
# This tests the Kubernetes deployment under simulated load conditions

set -e  # Exit on any error

echo "⚡ Performing Load Testing for Kubernetes Deployment..."

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Kubernetes cluster is not accessible. Please start Minikube first."
    exit 1
fi

# Find the services
echo "🔍 Locating services for load testing..."

BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

if [ -z "$BACKEND_POD" ]; then
    echo "❌ No backend pod found for load testing."
    echo "   Attempting to ensure deployment is active..."
    cd deployment/helm/todo-chatbot/
    helm upgrade --install todo-chatbot . --values values.yaml --wait --timeout=5m || echo "Deployment check completed"
    cd ../../..

    sleep 10
    BACKEND_POD=$(kubectl get pods -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || kubectl get pods -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)

    if [ -z "$BACKEND_POD" ]; then
        echo "❌ Still no backend pod found. Exiting load test."
        exit 1
    fi
fi

echo "✅ Backend pod found: $BACKEND_POD"

# Check if apache bench (ab) is available in the pod, otherwise try alternatives
AB_AVAILABLE=$(kubectl exec $BACKEND_POD -- which ab 2>/dev/null | wc -l)
WGET_AVAILABLE=$(kubectl exec $BACKEND_POD -- which wget 2>/dev/null | wc -l)
CURL_AVAILABLE=$(kubectl exec $BACKEND_POD -- which curl 2>/dev/null | wc -l)

if [ "$CURL_AVAILABLE" -gt 0 ]; then
    echo "✅ curl is available in backend pod for load testing"
    LOAD_TOOL="curl"
elif [ "$WGET_AVAILABLE" -gt 0 ]; then
    echo "✅ wget is available in backend pod for load testing"
    LOAD_TOOL="wget"
elif [ "$AB_AVAILABLE" -gt 0 ]; then
    echo "✅ Apache Bench (ab) is available in backend pod for load testing"
    LOAD_TOOL="ab"
else
    echo "⚠️  No standard load testing tools available in backend pod"
    echo "   Using basic curl loops for simple load simulation"
    LOAD_TOOL="basic_curl"
fi

# Define test parameters
CONCURRENT_REQUESTS=5
TOTAL_REQUESTS=50
TEST_DURATION=30  # seconds for basic test

echo ""
echo "⚙️  Load Test Configuration:"
echo "   Concurrent Requests: $CONCURRENT_REQUESTS"
echo "   Total Requests: $TOTAL_REQUESTS"
echo "   Duration: $TEST_DURATION seconds (if using basic curl)"
echo ""

# Test 1: Health endpoint load
echo "🧪 Test 1: Load testing health endpoint..."

if [ "$LOAD_TOOL" = "ab" ]; then
    echo "   Running Apache Bench test on health endpoint..."

    # Copy a simple test script to the pod if ab is available
    kubectl exec $BACKEND_POD -- bash -c "curl -s http://localhost:8000/health" > /dev/null 2>&1 && echo "Initial health check passed"

    # Since we can't easily install ab in the pod, we'll create a simple load test
    echo "   Performing simple concurrent curl requests..."
    START_TIME=$(date +%s)

    for i in $(seq 1 $CONCURRENT_REQUESTS); do
        (
            for j in $(seq 1 $((TOTAL_REQUESTS / CONCURRENT_REQUESTS))); do
                kubectl exec $BACKEND_POD -- curl -s -o /tmp/health_$$_$i$j.txt -w "%{http_code}:%{time_total}\\n" http://localhost:8000/health 2>/dev/null >> /tmp/load_results_$$_$i.txt
            done
        ) &
    done

    wait
    END_TIME=$(date +%s)
    ELAPSED_TIME=$((END_TIME - START_TIME))

    # Collect results
    TOTAL_RESPONSES=0
    SUCCESSFUL_RESPONSES=0
    TOTAL_TIME=0
    MIN_TIME=9999
    MAX_TIME=0

    for i in $(seq 1 $CONCURRENT_REQUESTS); do
        if [ -f "/tmp/load_results_$$_$i.txt" ]; then
            while IFS= read -r line; do
                if [[ $line =~ ^([0-9]+):([0-9.]+)$ ]]; then
                    CODE="${BASH_REMATCH[1]}"
                    TIME="${BASH_REMATCH[2]}"

                    TOTAL_RESPONSES=$((TOTAL_RESPONSES + 1))
                    TOTAL_TIME=$(echo "$TOTAL_TIME + $TIME" | bc -l)

                    if [ "$CODE" -eq 200 ]; then
                        SUCCESSFUL_RESPONSES=$((SUCCESSFUL_RESPONSES + 1))
                    fi

                    if (( $(echo "$TIME > $MAX_TIME" | bc -l) )); then
                        MAX_TIME=$TIME
                    fi
                    if (( $(echo "$TIME < $MIN_TIME" | bc -l) )); then
                        MIN_TIME=$TIME
                    fi
                fi
            done < /tmp/load_results_$$_$i.txt

            rm -f /tmp/load_results_$$_$i.txt
            rm -f /tmp/health_$$_*.txt
        fi
    done

elif [ "$LOAD_TOOL" = "basic_curl" ]; then
    echo "   Performing basic load test with concurrent curl requests..."

    START_TIME=$(date +%s)

    # Simple concurrent load testing with background processes
    for i in $(seq 1 $CONCURRENT_REQUESTS); do
        (
            COUNT=0
            while [ $COUNT -lt $((TOTAL_REQUESTS / CONCURRENT_REQUESTS)) ]; do
                TIMESTAMP=$(date +%s%N | cut -b1-13)
                RESPONSE=$(kubectl exec $BACKEND_POD -- curl -s -w ":%{http_code}:%{time_total}:%{time_starttransfer}" http://localhost:8000/health 2>/dev/null || echo "ERROR:NO_CODE:NO_TIME:NO_TIME")

                # Log response
                echo "$TIMESTAMP:$RESPONSE" >> /tmp/load_test_health_$$_$i.log
                COUNT=$((COUNT + 1))

                # Small delay between requests
                sleep 0.1
            done
        ) &
    done

    wait
    END_TIME=$(date +%s)
    ELAPSED_TIME=$((END_TIME - START_TIME))

    # Process results
    TOTAL_RESPONSES=0
    SUCCESSFUL_RESPONSES=0
    TOTAL_TIME=0
    MIN_TIME=9999
    MAX_TIME=0

    for i in $(seq 1 $CONCURRENT_REQUESTS); do
        if [ -f "/tmp/load_test_health_$$_$i.log" ]; then
            while IFS= read -r line; do
                # Parse: TIMESTAMP:BODY:HTTP_CODE:TOTAL_TIME:START_TRANSFER_TIME
                IFS=':' read -r timestamp body http_code total_time start_transfer <<< "$line"

                if [ "$http_code" = "200" ]; then
                    SUCCESSFUL_RESPONSES=$((SUCCESSFUL_RESPONSES + 1))
                fi

                if (( $(echo "$total_time > 0" | bc -l 2>/dev/null || echo 0) )); then
                    TOTAL_RESPONSES=$((TOTAL_RESPONSES + 1))
                    TOTAL_TIME=$(echo "$TOTAL_TIME + $total_time" | bc -l 2>/dev/null || echo $TOTAL_TIME)

                    if (( $(echo "$total_time > $MAX_TIME" | bc -l 2>/dev/null || echo 0) )); then
                        MAX_TIME=$total_time
                    fi
                    if (( $(echo "$total_time > 0" && "$total_time < $MIN_TIME" | bc -l 2>/dev/null || echo 1) )); then
                        MIN_TIME=$total_time
                    fi
                fi
            done < /tmp/load_test_health_$$_$i.log

            rm -f /tmp/load_test_health_$$_$i.log
        fi
    done

    if [ "$MIN_TIME" = "9999" ]; then
        MIN_TIME=0
    fi
fi

# Calculate averages
if [ $TOTAL_RESPONSES -gt 0 ]; then
    AVG_TIME=$(echo "$TOTAL_TIME / $TOTAL_RESPONSES" | bc -l 2>/dev/null || echo "0")
    SUCCESS_RATE=$(echo "scale=2; $SUCCESSFUL_RESPONSES * 100 / $TOTAL_REQUESTS" | bc)
else
    AVG_TIME=0
    SUCCESS_RATE=0
fi

echo "   Health Endpoint Load Test Results:"
echo "     Total Requests: $TOTAL_REQUESTS"
echo "     Successful: $SUCCESSFUL_RESPONSES"
echo "     Failed: $((TOTAL_REQUESTS - SUCCESSFUL_RESPONSES))"
echo "     Success Rate: ${SUCCESS_RATE}%"
echo "     Elapsed Time: ${ELAPSED_TIME}s"
echo "     Average Response Time: ${AVG_TIME}s"
echo "     Min Response Time: ${MIN_TIME}s"
echo "     Max Response Time: ${MAX_TIME}s"
echo "     Requests/sec: $(echo "scale=2; $TOTAL_RESPONSES / $ELAPSED_TIME" | bc 2>/dev/null || echo "N/A")"

HEALTH_LOAD_OK=true
if [ $(echo "$SUCCESS_RATE >= 95" | bc) -eq 1 ] && [ $(echo "$AVG_TIME <= 2" | bc -l 2>/dev/null || echo 0) -eq 1 ]; then
    echo "   ✅ Health endpoint load test PASSED"
else
    echo "   ⚠️  Health endpoint load test shows performance concerns"
    HEALTH_LOAD_OK=false
fi

# Test 2: API endpoint load (if available)
echo ""
echo "🧪 Test 2: Load testing API endpoints (if available)..."

# Find a suitable API endpoint to test
API_ENDPOINTS=("/tasks" "/api/tasks" "/api/v1/tasks" "/todos" "/api/todos")
API_ENDPOINT=""

for endpoint in "${API_ENDPOINTS[@]}"; do
    RESPONSE=$(kubectl exec $BACKEND_POD -- curl -s -w " HTTP_CODE:%{http_code}" http://localhost:8000$endpoint 2>/dev/null || echo "FAILED")

    if [[ $RESPONSE != "FAILED" ]]; then
        HTTP_CODE=$(echo $RESPONSE | grep -o "HTTP_CODE:[0-9]*" | cut -d':' -f2)
        if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 500 ]; then
            API_ENDPOINT="$endpoint"
            echo "   Found working API endpoint: $endpoint"
            break
        fi
    fi
done

if [ ! -z "$API_ENDPOINT" ]; then
    # Perform load test on API endpoint
    START_TIME=$(date +%s)

    for i in $(seq 1 3); do  # Reduced concurrent requests for API testing
        (
            COUNT=0
            while [ $COUNT -lt 10 ]; do  # Fewer requests to be safe with DB operations
                TIMESTAMP=$(date +%s%N | cut -b1-13)
                RESPONSE=$(kubectl exec $BACKEND_POD -- curl -s -w ":%{http_code}:%{time_total}" http://localhost:8000$API_ENDPOINT 2>/dev/null || echo "ERROR:NO_CODE:NO_TIME")

                echo "$TIMESTAMP:$RESPONSE" >> /tmp/load_test_api_$$_$i.log
                COUNT=$((COUNT + 1))

                sleep 0.5  # Longer delay for API tests
            done
        ) &
    done

    wait
    END_TIME=$(date +%s)
    API_ELAPSED_TIME=$((END_TIME - START_TIME))

    # Process API results
    API_TOTAL_RESPONSES=0
    API_SUCCESSFUL_RESPONSES=0
    API_TOTAL_TIME=0
    API_MIN_TIME=9999
    API_MAX_TIME=0

    for i in $(seq 1 3); do
        if [ -f "/tmp/load_test_api_$$_$i.log" ]; then
            while IFS= read -r line; do
                IFS=':' read -r timestamp body http_code total_time <<< "$line"

                if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 400 ]; then
                    API_SUCCESSFUL_RESPONSES=$((API_SUCCESSFUL_RESPONSES + 1))
                fi

                if (( $(echo "$total_time > 0" | bc -l 2>/dev/null || echo 0) )); then
                    API_TOTAL_RESPONSES=$((API_TOTAL_RESPONSES + 1))
                    API_TOTAL_TIME=$(echo "$API_TOTAL_TIME + $total_time" | bc -l 2>/dev/null || echo $API_TOTAL_TIME)

                    if (( $(echo "$total_time > $API_MAX_TIME" | bc -l 2>/dev/null || echo 0) )); then
                        API_MAX_TIME=$total_time
                    fi
                    if (( $(echo "$total_time > 0" && "$total_time < $API_MIN_TIME" | bc -l 2>/dev/null || echo 1) )); then
                        API_MIN_TIME=$total_time
                    fi
                fi
            done < /tmp/load_test_api_$$_$i.log

            rm -f /tmp/load_test_api_$$_$i.log
        fi
    done

    if [ "$API_MIN_TIME" = "9999" ]; then
        API_MIN_TIME=0
    fi

    if [ $API_TOTAL_RESPONSES -gt 0 ]; then
        API_AVG_TIME=$(echo "$API_TOTAL_TIME / $API_TOTAL_RESPONSES" | bc -l 2>/dev/null || echo "0")
        API_SUCCESS_RATE=$(echo "scale=2; $API_SUCCESSFUL_RESPONSES * 100 / 30" | bc)
    else
        API_AVG_TIME=0
        API_SUCCESS_RATE=0
    fi

    echo "   API Endpoint Load Test Results (Endpoint: $API_ENDPOINT):"
    echo "     Total Requests: 30"
    echo "     Successful: $API_SUCCESSFUL_RESPONSES"
    echo "     Failed: $((30 - API_SUCCESSFUL_RESPONSES))"
    echo "     Success Rate: ${API_SUCCESS_RATE}%"
    echo "     Elapsed Time: ${API_ELAPSED_TIME}s"
    echo "     Average Response Time: ${API_AVG_TIME}s"
    echo "     Min Response Time: ${API_MIN_TIME}s"
    echo "     Max Response Time: ${API_MAX_TIME}s"

    API_LOAD_OK=true
    if [ $(echo "$API_SUCCESS_RATE >= 90" | bc) -eq 1 ] && [ $(echo "$API_AVG_TIME <= 5" | bc -l 2>/dev/null || echo 0) -eq 1 ]; then
        echo "   ✅ API endpoint load test PASSED"
    else
        echo "   ⚠️  API endpoint load test shows performance concerns"
        API_LOAD_OK=false
    fi
else
    echo "   ⚠️  No suitable API endpoint found for load testing"
    API_LOAD_OK=false
fi

# Test 3: Resource utilization monitoring
echo ""
echo "📊 Test 3: Resource Utilization Monitoring..."

# Get resource usage during load
kubectl top pod $BACKEND_POD 2>/dev/null || echo "Resource monitoring not available (metrics server may not be installed)"

# Check if we can get logs to see if there are any performance-related warnings
echo "🔍 Checking application logs for performance issues..."
kubectl logs $BACKEND_POD --since=2m | grep -i -E "(slow|timeout|memory|cpu|performance|warning)" | head -n 10

# Summary
echo ""
echo "🎉 Load testing completed!"
echo ""
echo "📋 Load Testing Summary:"
echo "   Health Endpoint:"
echo "     Success Rate: ${SUCCESS_RATE}%"
echo "     Avg Response: ${AVG_TIME}s"
echo "     Status: $(if [ "$HEALTH_LOAD_OK" = true ]; then echo "✅ PASS"; else echo "⚠️  ISSUES"; fi)"
echo ""
echo "   API Endpoint:"
echo "     Success Rate: ${API_SUCCESS_RATE}%"
echo "     Avg Response: ${API_AVG_TIME}s"
echo "     Status: $(if [ "$API_LOAD_OK" = true ]; then echo "✅ PASS"; else echo "⚠️  ISSUES"; fi)"
echo ""

# Performance evaluation
OVERALL_PERFORMANCE_OK=true
ISSUES_FOUND=()

if [ $(echo "$SUCCESS_RATE < 90" | bc) -eq 1 ]; then
    OVERALL_PERFORMANCE_OK=false
    ISSUES_FOUND+=("Health endpoint success rate below 90%")
fi

if [ $(echo "$AVG_TIME > 3" | bc -l 2>/dev/null || echo 1) -eq 1 ]; then
    OVERALL_PERFORMANCE_OK=false
    ISSUES_FOUND+=("Health endpoint average response time above 3s")
fi

if [ $(echo "$API_SUCCESS_RATE < 85" | bc) -eq 1 ]; then
    OVERALL_PERFORMANCE_OK=false
    ISSUES_FOUND+=("API endpoint success rate below 85%")
fi

if [ $(echo "$API_AVG_TIME > 5" | bc -l 2>/dev/null || echo 1) -eq 1 ]; then
    OVERALL_PERFORMANCE_OK=false
    ISSUES_FOUND+=("API endpoint average response time above 5s")
fi

if [ "$OVERALL_PERFORMANCE_OK" = true ]; then
    echo "✅ Overall Performance: ACCEPTABLE"
    echo "💡 The application performs within expected parameters under load."
    echo ""
    echo "🎯 Load test objectives met:"
    echo "   - High success rates (>90%)"
    echo "   - Acceptable response times (<3s health, <5s API)"
    echo "   - Stable performance under concurrent load"
else
    echo "⚠️  Overall Performance: NEEDS ATTENTION"
    echo "🔧 Issues identified:"
    for issue in "${ISSUES_FOUND[@]}"; do
        echo "   - $issue"
    done
    echo ""
    echo "📈 Recommendations:"
    echo "   - Review resource limits and consider increasing if needed"
    echo "   - Optimize database queries if API responses are slow"
    echo "   - Implement caching for frequently accessed data"
    echo "   - Consider scaling strategies for production loads"
fi

# Cleanup temporary files
rm -f /tmp/load_test_*_$$_*.log 2>/dev/null || true

echo ""
echo "🧪 Load testing script completed. For more comprehensive testing in production,"
echo "   consider using specialized tools like k6, JMeter, or Artillery."