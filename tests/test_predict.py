from PIL import Image
from unittest.mock import patch
import torch

from app.predict import predict, CLASS_NAMES


def test_predict_success(fake_image, fake_model):
    """
    Predict returns PredictionResponse with correct class and confidence
    """
    image = Image.open(fake_image)

    with patch("classify_tumor.predict._load_model", return_value=fake_model), \
        patch("classify_tumor.predict._get_device", return_value=torch.device("cpu")):

        result = predict(image)

    assert result.predicted_class in CLASS_NAMES
    assert result.predicted_class == "malignant"
    assert isinstance(result.confidence, float)
    assert 0.0 <= result.confidence <= 1.0


def test_predict_confidence_rounding(fake_image, fake_model):
    """
    Confidence is rounded to 2 decimals
    """
    image = Image.open(fake_image)

    with patch("classify_tumor.predict._load_model", return_value=fake_model), \
        patch("classify_tumor.predict._get_device", return_value=torch.device("cpu")):

        result = predict(image)

    # softmax([0.1, 0.9]) ≈ 0.69
    assert result.confidence == round(result.confidence, 2)


def test_predict_calls_model_once(fake_image, fake_model):
    """
    Ensure model is called exactly once
    """
    image = Image.open(fake_image)

    with patch("classify_tumor.predict._load_model", return_value=fake_model), \
        patch("classify_tumor.predict._get_device", return_value=torch.device("cpu")):

        predict(image)

    fake_model.assert_called_once()