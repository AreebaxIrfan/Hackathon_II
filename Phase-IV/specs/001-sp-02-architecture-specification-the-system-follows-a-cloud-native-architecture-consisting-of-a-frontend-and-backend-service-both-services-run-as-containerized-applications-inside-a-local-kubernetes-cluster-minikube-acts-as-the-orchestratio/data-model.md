# Data Model: Cloud-Native Kubernetes Architecture

## Architecture Components

### Containerized Services

#### FrontendServiceContainer
- **image**: string (container image identifier)
- **port**: integer (port number for the frontend, typically 3000)
- **environment**: map<string, string> (environment variables for configuration)
- **resources**: ResourceRequirements (CPU and memory allocation)
- **healthChecks**: HealthCheckConfig (liveness and readiness probe configuration)
- **replicas**: integer (desired number of instances)
- **imagePullPolicy**: string (policy for pulling container images)

#### BackendServiceContainer
- **image**: string (container image identifier)
- **port**: integer (port number for the backend, typically 8000)
- **environment**: map<string, string> (environment variables for configuration)
- **resources**: ResourceRequirements (CPU and memory allocation)
- **healthChecks**: HealthCheckConfig (liveness and readiness probe configuration)
- **replicas**: integer (desired number of instances)
- **imagePullPolicy**: string (policy for pulling container images)

### Kubernetes Resources

#### DeploymentConfig
- **serviceName**: string (name of the service)
- **container**: FrontendServiceContainer | BackendServiceContainer (service configuration)
- **selectors**: map<string, string> (labels for pod selection)
- **strategy**: string (deployment strategy, e.g., RollingUpdate)
- **replicas**: integer (number of desired pods)

#### ServiceConfig
- **name**: string (name of the Kubernetes service)
- **type**: string (service type: ClusterIP, LoadBalancer, NodePort)
- **ports**: array<ServicePort> (port configurations)
- **selector**: map<string, string> (pod selector for the service)

#### ServicePort
- **port**: integer (service port)
- **targetPort**: integer (target port on pods)
- **protocol**: string (protocol, typically TCP)

### Resource Configuration

#### ResourceRequirements
- **requests**: ResourceList (requested resources)
- **limits**: ResourceList (maximum allowed resources)

#### ResourceList
- **cpu**: string (CPU resource value, e.g., "500m")
- **memory**: string (memory resource value, e.g., "512Mi")

#### HealthCheckConfig
- **livenessProbe**: ProbeConfig (configuration for liveness probe)
- **readinessProbe**: ProbeConfig (configuration for readiness probe)

#### ProbeConfig
- **path**: string (endpoint for HTTP health check)
- **port**: integer (port for health check)
- **initialDelaySeconds**: integer (delay before first probe)
- **periodSeconds**: integer (interval between probes)
- **timeoutSeconds**: integer (probe timeout duration)
- **failureThreshold**: integer (number of failures to consider unhealthy)

### Helm Chart Configuration

#### HelmChartConfig
- **name**: string (chart name)
- **version**: string (chart version)
- **appVersion**: string (application version)
- **values**: map<string, any> (default values for the chart)
- **templates**: array<TemplateFile> (template files for Kubernetes manifests)

#### TemplateFile
- **name**: string (template file name)
- **content**: string (Go template content)
- **destination**: string (where to place the generated file)

### Network Configuration

#### ServiceDiscoveryConfig
- **namespace**: string (Kubernetes namespace)
- **serviceName**: string (name of the service to discover)
- **port**: integer (port for the service)
- **protocol**: string (communication protocol)

#### LocalAccessConfig
- **minikubeServiceName**: string (name of service in Minikube)
- **localPort**: integer (port on local machine)
- **accessMethod**: string (method to access service: LoadBalancer, NodePort, PortForward)

## Relationships

### Service Communication
- FrontendServiceContainer → ServiceDiscoveryConfig (frontend discovers backend)
- BackendServiceContainer ← ServiceDiscoveryConfig (backend receives requests)

### Deployment Hierarchy
- DeploymentConfig → FrontendServiceContainer | BackendServiceContainer (deployment uses container config)
- ServiceConfig → DeploymentConfig (service exposes deployment)
- ResourceRequirements → DeploymentConfig (applies to container resources)
- HealthCheckConfig → DeploymentConfig (configures health checks)

### Helm Packaging
- HelmChartConfig → DeploymentConfig | ServiceConfig (chart packages Kubernetes configs)
- TemplateFile → HelmChartConfig (chart uses templates)

## State Transitions

### Container States
- **Pending**: Container being prepared for deployment
- **Running**: Container actively serving requests
- **Terminated**: Container has stopped (completed or failed)

### Deployment States
- **Progressing**: Deployment is being updated
- **Complete**: Deployment has finished successfully
- **Failed**: Deployment encountered an error

### Service States
- **Active**: Service is available and routing traffic
- **Inactive**: Service is not routing traffic (no healthy endpoints)
- **Updating**: Service configuration is being modified

## Validation Rules

### Container Configuration Validation
- image must not be empty
- port must be in valid range (1-65535)
- resource requests must not exceed limits
- health check path must start with "/"

### Kubernetes Service Validation
- service name must follow DNS label standard
- port numbers must be valid integers
- service type must be one of: ClusterIP, LoadBalancer, NodePort
- selector labels must match deployment labels

### Helm Chart Validation
- chart name must follow Helm naming conventions
- version must follow semantic versioning
- required values must be present
- template syntax must be valid