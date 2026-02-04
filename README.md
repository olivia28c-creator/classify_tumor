# Tumor Classification API (FastAPI + PyTorch)

This version of the project provides an API to classify image of skin tumors (benign/malignant).
It includes endpoints to upload images, obtain the HTML form and unit testing with pytest.
- ⁠API built with *FastAPI*.
- Standard preprocessing with *torchvision.transforms*.
- Structured logging with console outpout.
- Exception handling with `HTTPExceptions` from *FastAPI/Starlette*.
- Unit tests with *pytest*.

## Model context

The model was trained in a prior phase using **Transfer Learning**:

- **ResNet18 pre-trained** on ImageNet was used.
- The convolutional layers were frozen to leverage general image pattern recognition.
- The final linear layer was replaced to output **binary classification**: benign vs malignant tumor.
- The dataset used was from Kaggle: `fanconic/skin-cancer-malignant-vs-benign`.
- Data augmentation was applied to the training set (resize, random crop, horizontal flips) and basic normalization for the test set.
- Optimization with `Adadelta` and `CrossEntropyLoss`.
- Achieved ~82% accuracy on both training and test sets.

> Note: **Training code is not included** in this repository. Only the final weights (resnet_skin.pth) are included in the root directory for loading, with @lru_cache to avoid loading it for every client call.


---

## Installation and setup

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```
Download or clone the repository and its basic dependencies.

Using git:

```bash
git clone https://github.com/olivia28c-creator/classify_tumor
````
The repository will then be cloned into the current working directory. Then, go to the root of the `classify_tumor` repository and head to the branch _fast-api_:

```bash
git switch -q fast-api
```

If you do not use git, download the repository manually from the current branch (_fast-api_).

From the root of the `classify_tumor` repository, install basic dependencies:

```bash
pip install -r requirements.txt
```
Key dependencies:
- ⁠fastapi
- ⁠uvicorn
- ⁠torch
- torchvision
⁠- pillow
- ⁠pytest
- ⁠python-multipart

---

## Run the server

From the root directory:

```bash
uvicorn classify_tumor.main:app --reload
```
Or rather:

```bash
fastapi run classify_tumor/main.py
```
For development mode, use:
```bash
fastapi dev classify_tumor/main.py
```

The app will be served by default in the localhost IP address (127.0.0.1), port 8000:

[http://localhost:8000](http://localhost:8000)


---

## Endpoints

### *GET /*
Returns welcome message.
[http://localhost:8000/](http://localhost:8000/)

### *GET /predict/*
Returns a basic HTML form to upload the file.
[http://localhost:8000/predict](http://localhost:8000/predict)

### *POST /upload/*
Accepts an image file and returns the prediction.
[http://localhost:8000/upload](http://localhost:8000/upload)
> Note: This is a POST path operation. Opening it directly in the browser will show an error (405) because only GET requests can be accessed via URL, and this operation does not define a GET method.

**Response example:**

{
"predicted_class": "benign",
"confidence": 0.87
}

**Exceptions handled:**

- No file → 400 (Bad request)
- File is not a valid image → 400 (Bad request)
- Any other exception → 500 (Internal server error)

---

---

## Use example via curl


```bash
curl -X POST "http://localhost:8000/upload/" -F "file=@foto.jpg"
```

You can check all the API functionalities and complete documentation at:

[http://localhost:8000/docs](http://localhost:8000/docs)



---

## Tests

To run the tests, from root directory:

```bash
pytest
```



