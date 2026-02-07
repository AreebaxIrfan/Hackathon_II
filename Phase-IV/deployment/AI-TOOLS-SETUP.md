# AI-Assisted Tools Setup Guide

## Overview

This guide covers the installation and configuration of AI-assisted tools for Kubernetes deployment and management.

## Tools

### 1. Gordon (Docker AI)

**Purpose**: AI-assisted Docker operations and optimization

**Installation**:
```bash
# Gordon is typically installed via Docker Desktop extensions
# Or as a CLI tool - check latest installation method at:
# https://github.com/docker/gordon (if available)
```

**Usage**:
```bash
# Generate optimized Dockerfile
gordon create-dockerfile

# Optimize existing Dockerfile
gordon optimize Dockerfile

# Security scan
gordon scan <image-name>
```

**Alternative**: If Gordon is not available, use standard Docker best practices:
- Multi-stage builds
- Minimal base images (alpine, slim)
- Layer caching optimization
- Security scanning with `docker scan`

### 2. kubectl-ai

**Purpose**: AI-enhanced kubectl commands for easier Kubernetes management

**Installation**:
```bash
# Install kubectl-ai plugin
# Check latest installation at: https://github.com/sozercan/kubectl-ai

# Example installation (may vary):
kubectl krew install ai
```

**Usage**:
```bash
# Natural language queries
kubectl ai "show me all pods in default namespace"
kubectl ai "scale backend deployment to 3 replicas"
kubectl ai "get logs from frontend pods"
kubectl ai "describe deployment issues"
```

**Alternative**: Use standard kubectl commands with clear documentation

### 3. Kagent

**Purpose**: Kubernetes AI agent for cluster operations and monitoring

**Installation**:
```bash
# Kagent installation (check latest method)
# May be available as kubectl plugin or standalone tool
```

**Usage**:
```bash
# Cluster health analysis
kagent analyze cluster

# Performance optimization
kagent optimize resources

# Troubleshooting
kagent diagnose <pod-name>
```

**Alternative**: Use standard Kubernetes monitoring tools:
- `kubectl top nodes`
- `kubectl top pods`
- `kubectl describe`
- `kubectl logs`

## Configuration

### Environment Variables

Create a `.env` file in the deployment directory:

```bash
# AI Tool API Keys (if required)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Kubernetes Context
KUBECONFIG=~/.kube/config
KUBE_CONTEXT=minikube
```

### Kubectl Context

Ensure kubectl is configured for Minikube:

```bash
# Set context to minikube
kubectl config use-context minikube

# Verify context
kubectl config current-context
```

## Verification

Test that tools are working:

```bash
# Test Docker
docker --version
docker ps

# Test kubectl
kubectl version --client
kubectl cluster-info

# Test AI tools (if installed)
kubectl ai "list all namespaces"
```

## Fallback Strategy

If AI-assisted tools are not available:

1. **For Docker**: Use standard Docker commands with best practices
2. **For kubectl**: Use standard kubectl with good documentation
3. **For monitoring**: Use `kubectl top`, `kubectl describe`, and `kubectl logs`

## Notes

- AI-assisted tools are optional but recommended for easier management
- All operations can be performed with standard tools
- This project follows the constitution requirement for AI-first workflow
- Document any manual operations performed without AI assistance
