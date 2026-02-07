# Configurable Resource Allocation for Todo Chatbot Helm Chart

This document explains how to configure resource allocation for the Todo Chatbot application in Kubernetes using the Helm chart.

## Overview

The Todo Chatbot Helm chart provides extensive configuration options for resource allocation, scaling, and performance tuning. These configurations allow you to optimize the application for different environments (development, staging, production).

## Resource Configuration

### CPU and Memory Limits

Each service (backend and frontend) has configurable CPU and memory resources:

```yaml
backend:
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

frontend:
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
```

**Parameters explained:**
- `requests`: Minimum resources guaranteed to the container
- `limits`: Maximum resources the container can use
- `cpu`: CPU allocation (1000m = 1 CPU core)
- `memory`: Memory allocation (Mi = Mebibytes, Gi = Gibibytes)

### Example Configurations

#### Development (Minimal Resources)
```yaml
backend:
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 200m
      memory: 256Mi

frontend:
  resources:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 100m
      memory: 128Mi
```

#### Production (Recommended)
```yaml
backend:
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

frontend:
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
```

#### High-Traffic Production
```yaml
backend:
  replicaCount: 3
  resources:
    requests:
      cpu: 1000m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 2Gi

frontend:
  replicaCount: 3
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi
```

## Horizontal Pod Autoscaling (HPA)

The chart includes support for automatic scaling based on resource utilization:

```yaml
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80
```

**Parameters:**
- `enabled`: Whether to enable autoscaling
- `minReplicas`: Minimum number of pods
- `maxReplicas`: Maximum number of pods
- `targetCPUUtilizationPercentage`: Target CPU utilization for scaling
- `targetMemoryUtilizationPercentage`: Target memory utilization for scaling

## Volume Configuration

Configure additional volumes and mounts:

```yaml
extraVolumes:
  - name: logs
    emptyDir: {}

extraVolumeMounts:
  - name: logs
    mountPath: /var/log/app
    readOnly: false
```

## Node Selection and Affinity

Control where pods are scheduled:

```yaml
nodeSelector:
  kubernetes.io/os: linux
  kubernetes.io/arch: amd64

tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "frontend"
    effect: "NoSchedule"

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - todo-chatbot-frontend
        topologyKey: kubernetes.io/hostname
```

## Deployment Commands

### Apply Custom Resource Configuration

```bash
# Create a custom values file
cat > production-values.yaml << EOF
backend:
  replicaCount: 2
  resources:
    requests:
      cpu: 750m
      memory: 768Mi
    limits:
      cpu: 1500m
      memory: 1.5Gi

frontend:
  replicaCount: 2
  resources:
    requests:
      cpu: 300m
      memory: 384Mi
    limits:
      cpu: 600m
      memory: 768Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 8
  targetCPUUtilizationPercentage: 75
EOF

# Deploy with custom configuration
helm upgrade --install todo-chatbot . --values production-values.yaml
```

### Update Existing Deployment

```bash
# Update resources without downtime
helm upgrade todo-chatbot . --set backend.resources.requests.cpu=1000m --set backend.resources.limits.memory=2Gi
```

## Monitoring Resource Usage

Monitor resource utilization:

```bash
# Check resource usage
kubectl top pods

# Check resource limits
kubectl describe pod <pod-name>

# Monitor with custom metrics (if metrics server is installed)
kubectl get hpa
```

## Best Practices

1. **Start Conservative**: Begin with lower resource requests and increase based on monitoring
2. **Monitor Continuously**: Use monitoring tools to track actual usage vs. allocated resources
3. **Right-Size Gradually**: Adjust resources based on traffic patterns and performance metrics
4. **Use HPA**: Enable horizontal pod autoscaling for production workloads
5. **Set Realistic Limits**: Avoid setting limits too high or too low
6. **Plan for Growth**: Consider future traffic increases when setting maxReplicas

## Troubleshooting

### Pods in Pending State
- Check if nodes have sufficient resources
- Verify resource requests aren't higher than available capacity

### Application Performance Issues
- Increase resource requests/limits
- Enable HPA for automatic scaling
- Check for bottlenecks in database or external dependencies

### Scaling Issues
- Ensure metrics server is installed for HPA to work
- Verify target utilization percentages are reasonable
- Check that min/max replicas align with expected traffic patterns