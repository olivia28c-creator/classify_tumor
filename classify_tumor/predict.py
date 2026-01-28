from pathlib import Path
from typing import Dict

import torch
import logging
from torchvision import transforms
from PIL import Image


from classify_tumor.model import build_model
import importlib.resources as resources

# Classes in the same order as in the ImageFolder used during model training
CLASS_NAMES = ["benign", "malignant"]

logger = logging.getLogger(__name__)

def _get_device() -> torch.device:
    """Returns the device to use (MPS if available, otherwise CPU)."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")

def _load_model(device: torch.device) -> torch.nn.Module:
    model = build_model(num_classes=2)
    model.eval()
    model.to(device)

    model_path = (
        resources.files("classify_tumor.resources")
        .joinpath("resnet_skin.pth")
    )

    logger.debug("Loading model from %s", model_path)

    with model_path.open("rb") as f:
        state_dict = torch.load(f, map_location=device)

    model.load_state_dict(state_dict)
    return model

def _build_transforms() -> transforms.Compose:
    """Returns the transformations applied to the image before passing it to the model."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

def predict(image_path: Path) -> Dict[str, float | str]:
    """
    Performs inference on a tumor image.
    Assumes the path has already been validated; exceptions handled upstream.
    """

    # Opens image
    image = Image.open(image_path).convert("RGB")

    # Transforms
    transform = _build_transforms()
    tensor = transform(image).unsqueeze(0)  # add batch dimension
    device = _get_device()
    tensor = tensor.to(device)

    # Loads model
    model = _load_model(device)

    # Infers
    with torch.no_grad():
        outputs = model(tensor)
        probs = torch.softmax(outputs, dim=1)[0]
        confidence, pred_idx = torch.max(probs, dim=0)

    return {
        "label": CLASS_NAMES[pred_idx.item()],
        "confidence": confidence.item(),
    }