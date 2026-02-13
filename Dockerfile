# --- Imagen base ---
FROM python:3.11.7-slim

# --- Directorio de trabajo dentro del contenedor ---
WORKDIR /app

# --- Copiar dependencias y construir cache de pip ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copiar el código de la app ---
COPY . .

# --- Configurar cache de librerías ML (PyTorch, Transformers, etc.) para que no falle en /app ---
ENV XDG_CACHE_HOME=/tmp/.cache
RUN mkdir -p /tmp/.cache

# --- Usuario root para evitar problemas de permisos en macOS ---
# Puedes cambiar a un usuario no root más adelante en producción
USER root

# --- Exponer puerto 8000 ---
EXPOSE 8000

# --- Comando de arranque de FastAPI ---
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]