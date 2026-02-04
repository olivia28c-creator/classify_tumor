# classify_tumor

Python package to classify skin tumor images as benign or malignant using a pre-trained ResNet18 model. Includes a CLI, logging, path validation, and tests.
> Note: This is the principal branch (main) and contains the CLI version of the application. An ASGI version of the application is available in the fast-api branch of this repository, go to branches -> fast-api or follow the link: [https://github.com/olivia28c-creator/classify_tumor/tree/fast-api](https://github.com/olivia28c-creator/classify_tumor/tree/fast-api)

---

## Model Context

The model was trained in a prior phase using **Transfer Learning**:

- **ResNet18 pre-trained** on ImageNet was used.  
- The convolutional layers were frozen to leverage general image pattern recognition.  
- The final linear layer was replaced to output **binary classification**: benign vs malignant tumor.  
- The dataset used was from Kaggle: `fanconic/skin-cancer-malignant-vs-benign`.  
- Data augmentation was applied to the training set (resize, random crop, horizontal flips) and basic normalization for the test set.  
- Optimization with `Adadelta` and `CrossEntropyLoss`.  
- Achieved ~82% accuracy on both training and test sets.

> Note: **Training code is not included** in this repository. Only the final weights (`resnet_skin.pth`) are included in `classify_tumor/resources` for use in the CLI.

---

## Installation

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

Install the package with basic dependencies:

```bash
pip install .
```

For development (includes pytest):
```bash
pip install ".[dev]"
```
---

## Usage

From the terminal:

```bash
classify_tumor path/to/image.jpg
```

Optionally, for debug mode:

```bash
classify_tumor path/to/image.jpg -d
```

### Output

- Normal mode: prints only the label (`benign` or `malignant`) and the level of confidence 
- Debug mode: prints additional logging information useful for debugging

---

## Tests

Make sure to install dev dependencies
```bash
pip install ".[dev]"
```

Run the test suite:

```bash
pytest -v
```

Tests cover:
- Path and file type validation in service.py  
- Mocked inference in predict.py  
- Model integrity in model.py  
- CLI behavior

---

## Model Note

The `resnet_skin.pth` weigths are included in the package under `resources`, and it weigths about 45 MB.

- This model is **already trained** with the dataset described above.  
- The repository **does not include training code**.  
- For larger models or future updates, consider using **Git LFS** or external downloads.

---

## Requirements

- Python 3.10 or higher  
- torch  
- torchvision  
- Pillow  
- pytest (development only)
