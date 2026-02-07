# Backup and Recovery Procedures for Todo Chatbot

This document outlines the backup and recovery procedures for the Todo Chatbot application deployed on Kubernetes.

## Overview

Backup and recovery are critical for maintaining data integrity and ensuring business continuity. This guide covers procedures for backing up application data, configuration, and the ability to recover from various failure scenarios.

## Backup Strategies

### 1. Database Backups (Primary)

The most important data to back up is the PostgreSQL database containing user todos, preferences, and other application data.

#### Automated Database Backups

```bash
# Create a backup of the Neon PostgreSQL database
# This should be done using Neon's built-in backup features or pg_dump

# Example backup job manifest
apiVersion: batch/v1
kind: Job
metadata:
  name: postgres-backup
  namespace: default
spec:
  ttlSecondsAfterFinished: 3600  # Clean up after 1 hour
  template:
    spec:
      containers:
      - name: postgres-backup
        image: postgres:15
        env:
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: DATABASE_URL
        command:
        - /bin/sh
        - -c
        - |
          pg_dump $PGPASSWORD > /backups/todo-backup-$(date +%Y%m%d-%H%M%S).sql
          # Upload to cloud storage
          gsutil cp /backups/*.sql gs://your-backup-bucket/todo-chatbot/
        volumeMounts:
        - name: backup-storage
          mountPath: /backups
      volumes:
      - name: backup-storage
        persistentVolumeClaim:
          claimName: backup-pvc
      restartPolicy: Never
```

#### Manual Database Backup

```bash
# Connect to the database and create a dump
kubectl run pg-backup --image=postgres:15 --rm -it --restart=Never -- \
  bash -c 'pg_dump $DATABASE_URL' > backup-$(date +%Y%m%d).sql

# Store in a secure location
gsutil cp backup-$(date +%Y%m%d).sql gs://your-backup-bucket/todo-chatbot/
```

### 2. Kubernetes Configuration Backups

Back up all Kubernetes manifests and configurations:

```bash
# Back up all application configurations
kubectl get all,secret,configmap,pvc -o yaml > todo-chatbot-config-backup-$(date +%Y%m%d).yaml

# Back up Helm release information
helm get values todo-chatbot > todo-chatbot-values-backup-$(date +%Y%m%d).yaml
helm get manifest todo-chatbot > todo-chatbot-manifest-backup-$(date +%Y%m%d).yaml
```

### 3. Scheduled Backups with CronJob

Create automated backups using Kubernetes CronJobs:

```yaml
# postgres-backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup-cronjob
  namespace: default
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: postgres-backup
            image: postgres:15
            env:
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: database-secret
                  key: DATABASE_URL
            command:
            - /bin/sh
            - -c
            - |
              DATE=$(date +%Y%m%d_%H%M%S)
              FILENAME="todo-backup-$DATE.sql"

              # Dump database
              pg_dump $PGPASSWORD > "/backups/$FILENAME"

              # Compress
              gzip "/backups/$FILENAME"

              # Upload to cloud storage (adjust for your storage provider)
              gsutil cp "/backups/$FILENAME.gz" gs://your-backup-bucket/todo-chatbot/daily/

              # Clean up local file
              rm "/backups/$FILENAME.gz"

              # Keep only last 30 days of daily backups in cloud
              # (This would typically be handled by bucket lifecycle rules)
            volumeMounts:
            - name: backup-storage
              mountPath: /backups
          volumes:
          - name: backup-storage
            emptyDir: {}
          restartPolicy: OnFailure
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
```

Deploy the cron job:
```bash
kubectl apply -f postgres-backup-cronjob.yaml
```

## Recovery Procedures

### 1. Database Recovery

To recover from a database backup:

```bash
# Download the backup file
gsutil cp gs://your-backup-bucket/todo-chatbot/daily/backup-file.sql.gz ./
gunzip backup-file.sql.gz

# Create a recovery job
kubectl create configmap recovery-backup --from-file=backup.sql=./backup-file.sql

# Apply recovery job
kubectl apply -f - << EOF
apiVersion: batch/v1
kind: Job
metadata:
  name: postgres-restore
  namespace: default
spec:
  template:
    spec:
      containers:
      - name: postgres-restore
        image: postgres:15
        env:
        - name: PGPASSWORD
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: DATABASE_URL
        command:
        - /bin/sh
        - -c
        - |
          # Restore database
          psql $PGPASSWORD < /backup/backup.sql
        volumeMounts:
        - name: backup-volume
          mountPath: /backup
      volumes:
      - name: backup-volume
        configMap:
          name: recovery-backup
      restartPolicy: Never
EOF
```

### 2. Application Configuration Recovery

Restore Kubernetes configurations from backup:

```bash
# Apply backed up configurations
kubectl apply -f todo-chatbot-config-backup-$(date +%Y%m%d).yaml

# Or if using Helm, reinstall from backed up values
helm upgrade --install todo-chatbot ./deployment/helm/todo-chatbot/ --values todo-chatbot-values-backup-$(date +%Y%m%d).yaml
```

### 3. Complete Disaster Recovery

In case of complete cluster loss:

1. **Provision new cluster**:
   ```bash
   # For Minikube
   minikube start

   # For other providers, follow their cluster creation process
   ```

2. **Recreate secrets** (from your secure storage):
   ```bash
   # Recreate secrets from your secure backup location
   kubectl create secret generic database-secret --from-literal=DATABASE_URL=<your-db-url>
   kubectl create secret generic api-keys-secret --from-literal=OPENAI_API_KEY=<your-api-key> --from-literal=BETTER_AUTH_SECRET=<your-auth-secret>
   ```

3. **Restore database** from cloud backup to Neon

4. **Deploy application**:
   ```bash
   cd deployment/helm/todo-chatbot/
   helm install todo-chatbot . --values values.yaml --wait --timeout=10m
   ```

## Backup Storage and Retention Policies

### Storage Locations

- **Primary**: Cloud storage (Google Cloud Storage, AWS S3, Azure Blob Storage)
- **Secondary**: Encrypted backup to secondary cloud provider
- **Local**: For development/testing environments

### Retention Schedule

- **Daily backups**: Keep for 30 days
- **Weekly backups**: Keep for 3 months
- **Monthly backups**: Keep for 1 year
- **Annual backups**: Keep for 7 years (regulatory compliance)

### Backup Verification

Regularly verify backup integrity:

```bash
# Test restore to a temporary database
kubectl run backup-test --image=postgres:15 --rm -it --restart=Never -- \
  bash -c 'createdb test_restore && psql -d test_restore -f backup.sql && echo "Backup verified successfully"'
```

## Monitoring and Alerts

Set up monitoring for backup jobs:

```yaml
# backup-monitoring.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: backup-monitor
  namespace: default
spec:
  selector:
    matchLabels:
      app: backup-job
  endpoints:
  - port: metrics
    interval: 30s
---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: backup-alerts
  namespace: default
spec:
  groups:
  - name: backup.rules
    rules:
    - alert: BackupFailed
      expr: kube_job_status_failed{job_name=~"postgres-backup.*"} > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Database backup failed"
        description: "The database backup job {{ $labels.job_name }} has failed"
```

## Best Practices

1. **Test Regularly**: Regularly test your recovery procedures to ensure they work as expected
2. **Encrypt Backups**: Always encrypt sensitive backup data
3. **Offsite Storage**: Store backups in geographically distributed locations
4. **Access Control**: Restrict access to backup data to authorized personnel only
5. **Automation**: Automate backup processes to reduce human error
6. **Monitoring**: Monitor backup jobs and set up alerts for failures
7. **Documentation**: Keep recovery procedures well-documented and accessible
8. **Compliance**: Ensure backup retention policies comply with regulatory requirements

## Emergency Contacts and Procedures

- **Database Recovery**: Contact database administrator
- **Application Recovery**: Contact DevOps team
- **Cloud Provider Issues**: Contact cloud provider support
- **Security Incidents**: Follow incident response procedures

## Testing Your Backup Strategy

Create a test script to validate your backup and recovery procedures:

```bash
#!/bin/bash
# test-backup-recovery.sh

echo "🧪 Testing backup and recovery procedures..."

# 1. Create a test record in the database
echo "Creating test record..."
kubectl run test-record --image=busybox --rm -it --restart=Never -- \
  wget -qO- --post-data='{"title":"Backup Test Record","completed":false}' \
  --header='Content-Type:application/json' http://backend-service:8000/tasks

# 2. Create a backup
echo "Creating backup..."
# ... backup procedure ...

# 3. Modify the data to simulate a corruption
echo "Simulating data corruption..."
# ... corruption simulation ...

# 4. Restore from backup
echo "Restoring from backup..."
# ... restore procedure ...

# 5. Verify the test record is recovered
echo "Verifying recovery..."
kubectl run verify-recovery --image=busybox --rm -it --restart=Never -- \
  wget -qO- http://backend-service:8000/tasks | grep "Backup Test Record"

echo "✅ Backup and recovery test completed!"
```

Keep your backup and recovery procedures up to date as your application and infrastructure evolve.