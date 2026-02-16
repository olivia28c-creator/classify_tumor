# --- Etapa 1: Construir frontend ---
FROM node:20-alpine AS frontend

WORKDIR /frontend

# Copiar solo package.json y package-lock.json para cachear npm install
COPY frontend/package*.json .
RUN npm ci

# Copiar el resto del frontend y generar build
COPY frontend/ .
RUN npm run build
# Con vite se genera carpeta dist, con CRA carpeta build

# --- Etapa final: Backend + frontend estático ---
FROM python:3.11.7-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instalar dependencias de sistema necesarias
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias de Python
COPY requirements/base.txt requirements/
RUN pip install --no-cache-dir --upgrade pip --prefer-binary \
    && pip install --no-cache-dir -r requirements/base.txt

# Instalar PyTorch CPU only (ligero y portable en amd64/arm64)
RUN pip install --no-cache-dir --prefer-binary \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.10.0 torchvision==0.25.0

# Copiar backend
COPY app ./app

# Copiar archivos root necesarios
COPY resnet_skin.pth ./resnet_skin.pth

# Copiar build del frontend generado en la etapa anterior
COPY --from=frontend /frontend/dist ./frontend/dist

# Exponer puerto
EXPOSE 8000

# Comando para correr FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]