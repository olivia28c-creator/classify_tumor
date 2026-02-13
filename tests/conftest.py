from pathlib import Path
import pytest
from PIL import Image
import torch
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def fake_image(tmp_path: Path) -> Path:
    """
    Creates a fake image file for testing purposes.
    """
    img = Image.new("RGB", (224, 224), color="white")
    path = tmp_path / "test.jpg"
    img.save(path)
    return path

@pytest.fixture
def fake_non_image(tmp_path: Path) -> Path:
    """
    Crea un archivo que no es imagen para testear errores.
    """
    file_path = tmp_path / "dummy.txt"
    file_path.write_text("this is not an image")
    return file_path

@pytest.fixture
def fake_model():
    fake_output = torch.tensor([[0.1, 0.9]])

    model = MagicMock(return_value=fake_output)
    return model