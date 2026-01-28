import torch
from classify_tumor.model import build_model

def test_build_model_returns_torch_module():
    model = build_model(num_classes=2)
    assert isinstance(model, torch.nn.Module)

def test_build_model_output_layer_size():
    num_classes = 3
    model = build_model(num_classes=num_classes)
    assert model.fc.out_features == num_classes