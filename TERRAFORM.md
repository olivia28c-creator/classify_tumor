# 🧠 Skin Cancer Classifier - Cloud Infrastructure

Este repositorio contiene una aplicación Full-Stack (FastAPI + React) desplegada en **Google Cloud Platform** utilizando **Terraform** para la infraestructura y **Cloud Build** para la integración continua (CI/CD).

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener instalado:
1. [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. [Terraform](https://developer.hashicorp.com/terraform/downloads)
3. Un proyecto creado en [Google Cloud Console](https://console.cloud.google.com/).

## 🚀 Guía de Despliegue Rápido

### 1. Autenticación y APIs
Abre tu terminal y ejecuta estos comandos para identificarte y activar los servicios necesarios en tu proyecto:

```bash
# Login en Google Cloud
gcloud auth login
gcloud auth application-default login

# Configura tu proyecto actual
gcloud config set project TU_PROJECT_ID

# Activa las APIs necesarias
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    secretmanager.googleapis.com \
    artifactregistry.googleapis.com
````

### 2. Configuración de Variables
Entra en la carpeta terraform/ y crea un archivo llamado terraform.tfvars. Este archivo no se sube a GitHub (asegúrate de que esté en tu .gitignore).
```bash
# terraform/terraform.tfvars
project_id        = "tu-proyecto-id"
region            = "europe-west1"
db_password       = "tu-password-segura"
bucket_name       = "tu-nombre-unico-de-bucket"
github_repo_owner = "tu-usuario-github"
github_repo_name  = "tu-nombre-de-repo"
```
### 3. Levantar Infraestructura con Terraform
Desde la carpeta terraform/, ejecuta el despliegue automático de los recursos:
```bash
terraform init
terraform apply
```
Confirma con yes cuando te lo pida. Esto creará la Base de Datos, el Bucket, el repositorio de imágenes, los Secretos y el Disparador de Cloud Build.

### 4. Conexión Manual de GitHub
Por razones de seguridad y OAuth, Google requiere una conexión manual inicial por cada nuevo proyecto:

1. Ve a Cloud Build > Triggers en tu consola de GCP.
2. Haz clic en "Gestionar repositorios" > "Conectar repositorio".
3. Selecciona GitHub (Cloud Build GitHub App), autoriza y elige este repositorio.

### 5. Git Push y Despliegue Automático
Una vez conectado, cualquier cambio en la rama main disparará el despliegue:
```bash
git add .
git commit -m "🚀 Mi primer deploy automático"
git push origin main
````

### 🛠 Estructura del Proyecto
* `/app`: Backend FastAPI y lógica del modelo PyTorch.
* `/frontend`: Aplicación React (Vite).
* `/terraform`: Archivos de configuración de infraestructura (.tf).
* `cloudbuild.yaml`: Pipeline de CI/CD (Build de Docker y Deploy a Cloud Run).
* `Dockerfile`: Configuración Multi-stage para empaquetar la solución completa.

### ⚠️ Notas Importantes
* Archivo del Modelo: Tras el primer terraform apply, debes subir manualmente tu archivo resnet_skin.pth al Bucket de Storage creado para que la aplicación pueda cargarlo.
* Costes: Se utiliza una instancia db-f1-micro de Cloud SQL. Recuerda apagar o destruir los recursos con terraform destroy si no vas a usar la app para evitar cargos innecesarios.