from pathlib import Path
from unittest.mock import patch
import pytest

from classify_tumor.service import run_prediction


def test_run_prediction_happy_path(fake_image: Path):
    with patch("classify_tumor.service.predict") as mock_predict:
        mock_predict.return_value = {
            "label": "benign",
            "confidence": 0.95,
        }

        result = run_prediction(fake_image)

    mock_predict.assert_called_once_with(fake_image)
    assert result["label"] == "benign"


def test_run_prediction_file_not_found(tmp_path: Path):
    missing = tmp_path / "missing.jpg"

    with pytest.raises(FileNotFoundError):
        run_prediction(missing)


def test_run_prediction_is_directory(tmp_path: Path):
    with pytest.raises(IsADirectoryError):
        run_prediction(tmp_path)


def test_run_prediction_unsupported_extension(fake_non_image):
    with pytest.raises(ValueError):
        run_prediction(fake_non_image)