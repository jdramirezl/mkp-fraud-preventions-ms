# Deployment Guide

## Prerequisites

1. **Google Cloud Platform Setup**
   - Create a new project or use an existing one
   - Enable required APIs:
     - Cloud Run API
     - Cloud SQL Admin API
     - Artifact Registry API
   - Create a service account with necessary permissions
   - Download the service account key JSON

2. **GitHub Repository Setup**
   Add the following secrets:
   - `GCP_SA_KEY`: The service account key JSON
   - `PROJECT_ID`: Your GCP project ID

## Deployment Process

The deployment is fully automated through GitHub Actions and Terraform:

1. **CI/CD Pipeline** (.github/workflows/deploy.yml)
   - Runs on:
     - Pull requests (tests only)
     - Pushes to main/master (full deployment)
     - Manual triggers
   - Steps:
     - Runs tests and coverage
     - Builds Docker image
     - Pushes to Artifact Registry
     - Updates Cloud Run service

2. **Infrastructure** (terraform/)
   - Managed resources:
     - Cloud SQL PostgreSQL instance
     - Cloud Run service
     - IAM permissions
     - Network configuration

## Manual Deployment

If needed, you can deploy manually:

1. Build and push the Docker image:
```bash
docker build -t us-central1-docker.pkg.dev/PROJECT_ID/fraud-prevention/fraud-prevention-api:latest .
docker push us-central1-docker.pkg.dev/PROJECT_ID/fraud-prevention/fraud-prevention-api:latest
```

2. Apply Terraform configuration:
```bash
cd terraform
terraform init
terraform apply
```

## Security Considerations

1. **Database Security**
   - Cloud SQL instance with private IP
   - SSL/TLS encryption for connections
   - Managed backups and updates

2. **API Security**
   - HTTPS only
   - Cloud Run's built-in security
   - Input validation with Pydantic

3. **CI/CD Security**
   - Secrets managed via GitHub Actions
   - Least privilege service accounts
   - Container vulnerability scanning 