import os
import logging
from pathlib import Path
from functools import lru_cache

import torch
import torchvision
from torchvision import transforms
from PIL import Image
from google.cloud import storage

from app.schema import PredictionResponse

logger = logging.getLogger(__name__)

CLASS_NAMES = ["benign", "malignant"]

# CONFIGURACIÓN CLOUD
BUCKET_NAME = os.getenv("MODEL_BUCKET_NAME") # Bucket name in GCP
MODEL_FILENAME = os.getenv("MODEL_FILENAME")
LOCAL_MODEL_PATH = Path("/tmp") / MODEL_FILENAME # /tmp is the only writtable directory in Cloud Run

def download_model_from_gcs():
    """Downloads the model from Google Cloud Storage if it doesn't exist in /tmp"""
    if not LOCAL_MODEL_PATH.exists():
        logger.info(f"Downloading model from gs://{BUCKET_NAME}/{MODEL_FILENAME}...")
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(MODEL_FILENAME)
        blob.download_to_filename(LOCAL_MODEL_PATH)
        logger.info("Download completed")

@lru_cache
def _load_model() -> torch.nn.Module:
    # 1. Make sure model is available locally
    if BUCKET_NAME:
        download_model_from_gcs()
    
    # 2. Architecture
    model = torchvision.models.resnet18(weights=None)
    model.fc = torch.nn.Linear(512, len(CLASS_NAMES))
    
    # 3. Load weights
    path = LOCAL_MODEL_PATH if LOCAL_MODEL_PATH.exists() else Path(MODEL_FILENAME)
    
    model.load_state_dict(torch.load(path, map_location=torch.device("cpu")))
    model.eval()
    model.to(torch.device("cpu"))
    logger.info("Modelo cargado en memoria.")
    return model

IMAGE_TRANSFORMS = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict(image_input: Image.Image) -> PredictionResponse:

    model = _load_model()
    
    tensor = IMAGE_TRANSFORMS(image_input).unsqueeze(0).to(torch.device("cpu"))
    
    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)[0]
        confidence, pred_idx = torch.max(probs, dim=0)
    
    return PredictionResponse(
        predicted_class=CLASS_NAMES[pred_idx.item()], 
        confidence=round(float(confidence), 2)
    )