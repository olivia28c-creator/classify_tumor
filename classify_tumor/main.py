from fastapi import FastAPI
import logging

from classify_tumor.router_predict import router

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to the Tumor Classification API"}

    