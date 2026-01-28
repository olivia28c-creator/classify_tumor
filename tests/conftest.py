from pathlib import Path
import pytest
from PIL import Image

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