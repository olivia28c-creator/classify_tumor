
from unittest.mock import patch

def test_upload_success(client, fake_image):
    """
    Test happy path: valid image uploaded and prediction succeeds
    """
    fake_response = {
        "predicted_class": "tumor",
        "confidence": 0.95
    }

    with patch("classify_tumor.router_predict.predict", return_value=fake_response):
        with open(fake_image, "rb") as f:
            response = client.post(
                "/upload/",
                files={"file": ("test.jpg", f, "image/jpeg")}
            )

    assert response.status_code == 200
    assert response.json() == fake_response


def test_upload_no_file(client):
    """
    Test when no file is sent
    """
    response = client.post("/upload/")

    assert response.status_code == 400
    assert response.json()["detail"] == "No file uploaded"


def test_upload_non_image_file(client, fake_non_image):
    """
    Test when uploaded file is not a valid image
    """
    with open(fake_non_image, "rb") as f:
        response = client.post(
            "/upload/",
            files={"file": ("dummy.txt", f, "text/plain")}
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is not a valid image"


def test_predict_html_endpoint(client):
    """
    Test GET /predict/ returns HTML form
    """
    response = client.get("/predict/")

    assert response.status_code == 200
    assert "<form" in response.text
    assert 'type="file"' in response.text