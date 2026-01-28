from pathlib import Path
import logging

from classify_tumor.predict import predict

logger = logging.getLogger(__name__)

def run_prediction(image_path: Path) -> dict[str, float | str]:
    logger.debug("Service received path: %s", image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    if image_path.is_dir():
        raise IsADirectoryError(f"The provided path is a directory, not an image file: {image_path}")

    if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise ValueError(f"Unsupported image format: {image_path.suffix}")

    return predict(image_path)