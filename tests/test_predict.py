from pathlib import Path
from unittest.mock import patch, MagicMock
import torch
import pytest

from classify_tumor.predict import predict, CLASS_NAMES


def test_predict_happy_path(fake_image: Path):
    with patch("classify_tumor.predict._load_model") as mock_load_model:
        dummy_model = MagicMock()
        dummy_model.return_value = torch.tensor([[0.2, 0.8]])
        mock_load_model.return_value = dummy_model

        result = predict(fake_image)

    assert result["label"] in CLASS_NAMES
    assert 0.0 <= result["confidence"] <= 1.0


def test_predict_confidence_range(fake_image: Path):
    with patch("classify_tumor.predict._load_model") as mock_load_model:
        dummy_model = MagicMock()
        dummy_model.return_value = torch.tensor([[10.0, -10.0]])
        mock_load_model.return_value = dummy_model

        result = predict(fake_image)

    assert 0.0 <= result["confidence"] <= 1.0


def test_predict_returns_correct_label(fake_image: Path):
    with patch("classify_tumor.predict._load_model") as mock_load_model:
        dummy_model = MagicMock()
        dummy_model.return_value = torch.tensor([[0.9, 0.1]])
        mock_load_model.return_value = dummy_model

        result = predict(fake_image)

    assert result["label"] == "benign"


def test_predict_non_image_raises(fake_non_image):
    with pytest.raises(Exception):
        predict(fake_non_image)