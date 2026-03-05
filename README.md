# Tumor Classification API - Cloud Edition (GCP)

**Live Demo:** [https://classify-tumor-103742887581.europe-west1.run.app/](https://classify-tumor-103742887581.europe-west1.run.app/)

This branch contains the **infrastructure-as-code (IaC)** and **CI/CD configurations** required to deploy the Tumor Classification API automatically to Google Cloud Platform.

---

## Cloud Architecture

The deployment follows a modern serverless architecture:
* **Frontend & Backend:** Integrated into a single Docker container (Multi-stage build) and hosted on **Cloud Run**.
* **Infrastructure:** Managed via **Terraform** (Bucket, Secret Manager, Cloud Build Triggers).
* **CI/CD:** **Cloud Build** automatically triggers on every push to the `cloud` branch, building the image and deploying it.
* **Database:** Connected to **Cloud SQL (PostgreSQL)** for production-grade persistence.
* **Secrets:** Managed via **Secret Manager** (DB passwords).

---

## Prerequisites

Before deploying, ensure you have:
1. A **Google Cloud Project** with billing enabled.
2. The **gcloud CLI** installed and authenticated (`gcloud auth application-default login`).
3. **Terraform** installed (v1.0+).
4. A **GitHub repository** connected to your GCP project (via the Cloud Build "Manage Connections" page).

### Enable Google Cloud APIs
Before running Terraform, you must authenticate and enable the necessary services in your project:

```bash
# Login to Google Cloud
gcloud auth login
gcloud auth application-default login

# Enable required APIs
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    secretmanager.googleapis.com \
    artifactregistry.googleapis.com
```
### Manual GitHub Connection
For security reasons, Google requires a manual OAuth connection for the first time:
1. Go to **Cloud Build** > **Triggers** in your GCP Console.
2. Click **"Manage Repositories"** > **"Connect Repository"**.
3. Select **GitHub (Cloud Build GitHub App)**, authorize, and select this repository.

---

## Deployment Guide

### 1. Initialize Infrastructure (Terraform)
Navigate to the `terraform/` directory. Create a `terraform.tfvars` file (this file is git-ignored) and fill in your specific values:

```hcl
project_id        = "your-project-id"
region            = "europe-west1"
repository_name   = "your-artifact-registry-repo"
db_password       = "your-secure-password"
bucket_name       = "your-unique-model-bucket"
github_repo_owner = "your-github-username"
github_repo_name  = "your-github-repo-name"
file_name         = "your-model"
branch_name       = "^cloud$"
```

Then, run the following commands:

```bash
terraform init
terraform apply
```

> **Note on Permissions:** The Terraform script automatically configures the **Compute Service Account** with the necessary IAM roles (`Secret Manager Accessor`, `Cloud Run Admin`, `Log Writer`, etc.) to ensure the deployment doesn't fail due to "Permission Denied" errors.

### 2. The CI/CD Workflow
Once Terraform creates the trigger, any change pushed to the specified branch (by default, the `main` branch) will:
1. **Build** the Docker image using the `Dockerfile`.
2. **Push** the image to **Google Artifact Registry**.
3. **Deploy** a new revision to **Cloud Run**, automatically injecting secrets and environment variables.



To trigger it manually the first time:

```bash
gcloud builds submit --config cloudbuild.yaml .
```

## 📝 Key Files in this Branch

| File | Purpose |
| :--- | :--- |
| `terraform/main.tf` | Defines GCP resources (Bucket, Secrets, IAM, Triggers). |
| `cloudbuild.yaml` | The CI/CD pipeline instructions (Build, Push, Deploy). |
| `Dockerfile` | Multi-stage build (Node.js for React + Python for FastAPI). |

---

## ⚠️ Troubleshooting

### Permission Propagation Delay
When running Terraform for the first time, Google Cloud may take 1–2 minutes to propagate IAM permissions. This happens because Terraform might report the resource is "Created," but the IAM policy hasn't fully reached the Secret Manager service. If your first Cloud Build fails with a **403 Forbidden** error, wait a couple of minutes and **Retry** the build.

### Logging
To view logs during deployment or runtime:
* **Deployment logs:** Check the [Cloud Build Console](https://console.cloud.google.com/cloud-build/).
* **Application logs:** Check the [Cloud Run Logs](https://console.cloud.google.com/run/) (Filtered by `CLOUD_LOGGING_ONLY`).