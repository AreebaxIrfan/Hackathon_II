# Todo Chatbot Helm Chart

A Helm chart for deploying the Todo Chatbot application to Kubernetes. This chart packages both the frontend and backend services with configurable parameters.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Access to container images (todo-frontend and todo-backend)
- Database secrets configured (Neon PostgreSQL)
- API key secrets configured (OpenAI, Better Auth)

## Installation

### Quick Install

```bash
# Add the Helm repo (if published)
helm repo add todo-chatbot https://your-repo/charts

# Install the chart
helm install todo-chatbot deployment/helm/todo-chatbot/
```

### With Custom Values

```bash
# Install with custom configuration
helm install todo-chatbot deployment/helm/todo-chatbot/ --values my-values.yaml
```

### From Local Directory

```bash
# Navigate to chart directory
cd deployment/helm/todo-chatbot/

# Install the chart
helm install todo-chatbot . --values values.yaml
```

## Configuration

The following table lists the configurable parameters of the Todo Chatbot chart and their default values.

### Backend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.replicaCount` | Number of backend replicas | `1` |
| `backend.image.repository` | Backend image repository | `"todo-backend"` |
| `backend.image.tag` | Backend image tag | `"latest"` |
| `backend.image.pullPolicy` | Backend image pull policy | `"Never"` (for local Minikube) |
| `backend.service.type` | Backend service type | `"ClusterIP"` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.service.targetPort` | Backend container port | `8000` |
| `backend.resources.requests.cpu` | Backend CPU request | `"500m"` |
| `backend.resources.requests.memory` | Backend memory request | `"512Mi"` |
| `backend.resources.limits.cpu` | Backend CPU limit | `"1000m"` |
| `backend.resources.limits.memory` | Backend memory limit | `"1Gi"` |

### Frontend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.replicaCount` | Number of frontend replicas | `1` |
| `frontend.image.repository` | Frontend image repository | `"todo-frontend"` |
| `frontend.image.tag` | Frontend image tag | `"latest"` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `"Never"` (for local Minikube) |
| `frontend.service.type` | Frontend service type | `"LoadBalancer"` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.service.targetPort` | Frontend container port | `3000` |
| `frontend.resources.requests.cpu` | Frontend CPU request | `"200m"` |
| `frontend.resources.requests.memory` | Frontend memory request | `"256Mi"` |
| `frontend.resources.limits.cpu` | Frontend CPU limit | `"500m"` |
| `frontend.resources.limits.memory` | Frontend memory limit | `"512Mi"` |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `false` |
| `ingress.className` | Ingress class name | `"nginx"` |
| `ingress.hosts[0].host` | Hostname for ingress | `"todo-chatbot.local"` |
| `ingress.hosts[0].paths[0].path` | Path for frontend | `"/"` |
| `ingress.hosts[0].paths[0].pathType` | Path type | `"Prefix"` |

## Upgrading

```bash
# Upgrade with new values
helm upgrade todo-chatbot . --values values.yaml

# Upgrade with specific version
helm upgrade todo-chatbot . --version 1.1.0
```

## Uninstalling

```bash
# Uninstall the release
helm uninstall todo-chatbot
```

## Values File Example

```yaml
# Custom values file (my-values.yaml)
backend:
  replicaCount: 2
  resources:
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

frontend:
  replicaCount: 2
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 250m
      memory: 256Mi

ingress:
  enabled: true
  hosts:
    - host: my-todo-app.com
      paths:
        - path: /
          pathType: Prefix
```

## Secrets Required

The chart expects the following secrets to be created in the namespace:

- `database-secret`: Contains `DATABASE_URL`
- `api-keys-secret`: Contains `OPENAI_API_KEY` and `BETTER_AUTH_SECRET`

Create secrets manually or use your preferred secret management solution.

## Local Development

For local development with Minikube:

1. Build your Docker images and load them into Minikube:
   ```bash
   minikube image load todo-frontend:latest
   minikube image load todo-backend:latest
   ```

2. Install with local image pull policy:
   ```bash
   helm install todo-chatbot . --values values.yaml
   ```

## Troubleshooting

### Images not found
If you get `ErrImagePull` or `ImagePullBackOff`, ensure:
- Images are built and available
- `image.pullPolicy` is set correctly (`Never` for local Minikube, `Always` for registry)
- Image names/tags match your built images

### Secrets not found
Ensure required secrets exist in the target namespace:
```bash
kubectl get secrets
```

### Ingress not working
- Verify ingress controller is installed (e.g., NGINX Ingress Controller)
- Check ingress controller logs
- Verify DNS resolution for ingress hosts

## Contributing

To contribute to this Helm chart:

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test locally
5. Submit a pull request