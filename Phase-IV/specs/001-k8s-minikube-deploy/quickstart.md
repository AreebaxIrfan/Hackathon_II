# Quickstart Guide: Phase IV - Local Kubernetes Deployment

## Prerequisites

Before deploying the Todo Chatbot application to your local Kubernetes cluster, ensure you have the following tools installed:

- Docker Desktop (with Kubernetes enabled) or Docker Engine + kubectl
- Minikube
- Helm v3
- kubectl
- Gordon (Docker AI assistant)
- kubectl-ai (AI-enhanced kubectl)
- Kagent (Kubernetes AI agent)

## Setup Instructions

### 1. Start Minikube Cluster

```bash
minikube start
```

### 2. Clone the Repository

```bash
# If you haven't already cloned the repository
git clone [repository-url]
cd [repository-name]
```

### 3. Prepare the Application

The Todo Chatbot application consists of two parts:
- **Frontend**: Next.js application in the `./frontend` directory
- **Backend**: FastAPI application in the `./backend` directory

### 4. Containerize the Applications using Gordon

#### For the Backend:
```bash
cd ./backend
gordon create-dockerfile
```

#### For the Frontend:
```bash
cd ../frontend
gordon create-dockerfile
```

### 5. Build and Tag Docker Images

```bash
# Build backend image
docker build -t todo-chatbot-backend:latest ./backend

# Build frontend image
docker build -t todo-chatbot-frontend:latest ./frontend
```

### 6. Create Helm Chart

```bash
helm create todo-chatbot
```

### 7. Deploy Using Helm

```bash
helm install todo-chatbot ./todo-chatbot
```

## AI-Assisted Deployment Commands

Instead of manual commands, you can use AI-assisted tools:

### Using kubectl-ai:
```bash
# Get cluster status
kubectl-ai "show me the status of my cluster"

# Check running pods
kubectl-ai "show me all pods in the default namespace"
```

### Using Kagent:
```bash
# Scale the backend deployment
kagent "scale backend deployment to 3 replicas"
```

## Verify Deployment

### 1. Check Running Pods:
```bash
kubectl get pods
```

### 2. Check Services:
```bash
kubectl get services
```

### 3. Access the Application:
```bash
minikube service todo-chatbot-frontend --url
```

## Troubleshooting

### Common Issues:

1. **Pods stuck in Pending state**: Check if Minikube has sufficient resources allocated
2. **Service not accessible**: Verify that the ports are correctly configured
3. **ImagePullBackOff**: Ensure the Docker images are built and tagged correctly

### AI-Assisted Troubleshooting:
```bash
kubectl-ai "describe pods and show me any issues"
```

## Clean Up

To remove the deployment:
```bash
helm uninstall todo-chatbot
```

To stop Minikube:
```bash
minikube stop
```

## Next Steps

Once the deployment is successful, you can:
- Configure ingress to access the application at specific URLs
- Set up persistent storage for the database
- Configure environment variables for the applications
- Implement health checks and readiness probes