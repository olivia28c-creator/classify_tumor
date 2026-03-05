provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "bucket" {
  name     = var.bucket_name
  location = var.region
}

resource "google_secret_manager_secret" "db_pass" {
  secret_id = "DB_PASSWORD"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_pass_val" {
  secret      = google_secret_manager_secret.db_pass.id
  secret_data = var.db_password
}

# --- Automatic trigger ---
resource "google_cloudbuild_trigger" "github_trigger" {
  name     = "deploy-on-push"
  location = var.region
  service_account = "projects/${var.project_id}/serviceAccounts/${data.google_project.project.number}-compute@developer.gserviceaccount.com"
  
  github {
    owner = "olivia28c-creator"
    name  = "classify_tumor" # Asegúrate que sea EXACTO al nombre en la URL de GitHub
    push {
      branch = var.branch_name
    }
  }

  filename = "cloudbuild.yaml"

  substitutions = {
    _REGION      = var.region
    _BUCKET_NAME = var.bucket_name
    _REPO_NAME   = var.repository_name
    _FILE_NAME   = var.file_name
  }
}

# --- Automatic permits ---
# Configures IAM permits for the COMPUTE service account
resource "google_project_iam_member" "cloudbuild_roles" {
  for_each = toset([
    "roles/secretmanager.secretAccessor", # Para leer la contraseña de la DB
    "roles/run.admin",                    # Para crear/actualizar Cloud Run
    "roles/iam.serviceAccountUser",       # Para actuar como la cuenta de servicio
    "roles/cloudsql.client",              # Para conectar con la base de datos
    "roles/logging.logWriter"            
  ])
  
  project = var.project_id
  role    = each.key
  
  # CAMBIO CLAVE: Usamos la cuenta de Compute que identificamos antes
  member  = "serviceAccount:${data.google_project.project.number}-compute@developer.gserviceaccount.com"
}

data "google_project" "project" {
  project_id = var.project_id
}