from pathlib import Path
import torch
from functools import lru_cache
import torchvision
from torchvision import transforms
from PIL import Image
import os
import logging

from app.schema import PredictionResponse

logger = logging.getLogger(__name__)

# Classes in the same order as in the ImageFolder used during model training
CLASS_NAMES = ["benign", "malignant"]

MODEL_PATH = Path(os.getenv("MODEL_PATH", "resnet_skin.pth"))

def _get_device() -> torch.device:
    """Returns the device to use (MPS if available, otherwise CPU)."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")

@lru_cache
def _load_model() -> torch.nn.Module:
    """
    Load the pretrained model
    """
    model = torchvision.models.resnet18(
        weights=torchvision.models.ResNet18_Weights.DEFAULT
    )
    device = _get_device()
    model.fc = torch.nn.Linear(512, 2)
    model.eval()
    model.to(device = device)

    with MODEL_PATH.open("rb") as f:
        state_dict = torch.load(f, map_location = device)

    model.load_state_dict(state_dict)
    logger.debug("Model loaded successfully")
    return model

def _build_transforms() -> transforms.Compose:
    """Returns the transformations applied to the image before passing it to the model."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

def predict(image_input: Image) -> PredictionResponse:
    """
    Performs inference on a tumor image.
    Accepts Path, bytes, or file path string.
    """
    
    transform = _build_transforms()
    tensor = transform(image_input).unsqueeze(0)
    device = _get_device()
    tensor = tensor.to(device)
    
    model = _load_model()
    
    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)[0]
        confidence, pred_idx = torch.max(probs, dim=0)
    
    predicted_class = CLASS_NAMES[pred_idx.item()]
    response = PredictionResponse(
        predicted_class=predicted_class, 
        confidence=round(confidence.item(), 2)
    )
    
    return response