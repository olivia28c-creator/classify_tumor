# Stage 1: Build frontend
FROM node:20-alpine AS frontend

WORKDIR /frontend

# Copy only package.json and package-lock.json to cache npm install
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend and build
COPY frontend/ ./
RUN npm run build
# With vite: dist, with CRA: build

# Final stage: Backend + static frontend
FROM python:3.11.7-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies of Python
COPY requirements/base.txt requirements/
RUN pip install --no-cache-dir --upgrade pip --prefer-binary \
    && pip install --no-cache-dir -r requirements/base.txt

# Install PyTorch CPU only (light and portable in amd64/arm64)
RUN pip install --no-cache-dir --prefer-binary \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.10.0 torchvision==0.25.0

# Copy backend
COPY app ./app

# Copy build from the frontend generated in the previous stage
COPY --from=frontend /frontend/dist ./frontend/dist

# Expose port
EXPOSE 8080

# Command to run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]