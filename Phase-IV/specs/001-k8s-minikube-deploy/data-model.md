# Data Model: Phase IV - Local Kubernetes Deployment

## Overview
This document describes the key entities involved in the Kubernetes deployment of the Todo Chatbot application. Since this is an infrastructure deployment feature, the entities relate to Kubernetes resources and deployment artifacts rather than application data models.

## Key Entities

### Deployment
**Description**: Kubernetes resource defining the desired state for running application containers
- **Attributes**:
  - replicas (int): Number of pod instances to maintain
  - image (string): Container image reference
  - resources (object): CPU and memory limits/requests
  - env (array): Environment variables for the container
  - ports (array): Port mappings for the container
  - livenessProbe (object): Health check configuration
  - readinessProbe (object): Readiness check configuration

### Service
**Description**: Kubernetes resource providing network access to deployed pods
- **Attributes**:
  - type (string): Service type (ClusterIP, NodePort, LoadBalancer)
  - selector (object): Labels to match pods
  - ports (array): Port exposed by the service
  - clusterIP (string): Internal IP address (if applicable)

### Helm Chart
**Description**: Package format for Kubernetes applications containing templates and configuration
- **Attributes**:
  - name (string): Chart name
  - version (string): Chart version
  - description (string): Chart description
  - dependencies (array): Chart dependencies
  - templates (array): Kubernetes manifest templates
  - values (object): Default configuration values

### Container Image
**Description**: Packaged application artifacts stored in Docker registry for deployment
- **Attributes**:
  - repository (string): Image repository name
  - tag (string): Image version tag
  - digest (string): Image checksum
  - size (int): Image size in bytes

## Relationships
- A Helm Chart contains multiple Deployment and Service resources
- A Deployment manages multiple Pod instances
- A Service exposes a Deployment to network traffic
- Container Images are referenced by Deployments

## Validation Rules
- Deployment resource requests must not exceed limits
- Service selectors must match labels on target Deployments
- Helm chart values must be valid YAML
- Container image tags must follow semantic versioning

## State Transitions
- Deployment: Pending → Running → Terminated
- Service: Creating → Active → Deleting
- Helm Release: Deployed → Upgraded → Deleted
- Pod: Pending → Running → Succeeded/Terminated