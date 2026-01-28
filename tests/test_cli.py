import subprocess
import sys

def test_cli_no_arguments():
    result = subprocess.run(
        [sys.executable, "-m", "classify_tumor"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0

def test_cli_nonexistent_image():
    result = subprocess.run(
        [sys.executable, "-m", "classify_tumor", "does_not_exist.jpg"],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
    assert "Image not found" in result.stderr or "Image not found" in result.stdout

def test_cli_invalid_image(tmp_path):
    fake_file = tmp_path / "not_image.txt"
    fake_file.write_text("hello")

    result = subprocess.run(
        [sys.executable, "-m", "classify_tumor", str(fake_file)],
        capture_output=True,
        text=True
    )
    assert result.returncode != 0
    assert "Unsupported image format" in result.stderr or "Unsupported image format" in result.stdout