
from fastapi import APIRouter, UploadFile, HTTPException, status, File
from fastapi.responses import HTMLResponse
from typing import Union, Annotated
from PIL import Image, UnidentifiedImageError
import io
import logging

from sqlalchemy.orm import Session

from app.predict import predict
from app.schema import PredictionResponse
from app.db.models import Prediction

logger = logging.getLogger(__name__)

# Initialize FastAPI app
router = APIRouter()

from app.db.database import SessionLocal
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/")
async def classify(file: Annotated[
        Union[UploadFile, None],
        File(description="File as UploadFile")] = None,
        db: Session = Depends(get_db)) -> PredictionResponse:
    
    if file is None:
        logger.warning("No file uploaded for classification")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded")
    
    logger.info(f"Processing file: {file.filename}")

    try:

        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        prediction = predict(image)  # ← Cambiar predict para aceptar bytes
        
        db_prediction = Prediction(
        filename=file.filename,
        predicted_class=prediction.predicted_class,
        probability=prediction.confidence
    )

        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)

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

@router.get("/predictions")
def get_predictions(db: Session = Depends(get_db)):
    return db.query(Prediction).all()
