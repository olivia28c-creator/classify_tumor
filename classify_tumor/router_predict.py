
from fastapi import APIRouter, UploadFile, HTTPException, status, File
from fastapi.responses import HTMLResponse
from typing import Union, Annotated
from PIL import Image, UnidentifiedImageError
import io
import logging

from classify_tumor.predict import predict
from classify_tumor.schema import PredictionResponse

logger = logging.getLogger(__name__)

# Initialize FastAPI app
router = APIRouter()

@router.post("/upload/")
async def classify(file: Annotated[
        Union[UploadFile, None], File(description="File as UploadFile")] = None) -> PredictionResponse:
    if file is None:
        logger.warning("No file uploaded for classification")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded")
    
    logger.info(f"Processing file: {file.filename}")

    try:
        # LEER el archivo ANTES de pasar a predict (con AWAIT)
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Llamar a predict pasando los bytes
        prediction = predict(image)  # ← Cambiar predict para aceptar bytes
        
        logger.info(f"Prediction successful: {prediction}")
        return prediction
    except UnidentifiedImageError:
        message = "Uploaded file is not a valid image"
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Prediction failed")

@router.get("/predict/")
async def main():
    content = """
            <body>
            <form action="/upload/" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input type="submit">
            </form>
            </body>
    """
    return HTMLResponse(content=content)