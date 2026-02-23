import os
from fastapi import FastAPI
import logging
from fastapi.staticfiles import StaticFiles

from app.router_predict import router

logger = logging.getLogger(__name__)

from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tumor Classification API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.include_router(router, prefix="/api") 


@app.get("/api/health")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Tumor Classification API"}

if os.path.isdir("frontend/dist"): # En producción
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
else: # Desarrollo
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True)

