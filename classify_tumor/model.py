import torch
import torchvision

def build_model(num_classes: int = 2) -> torch.nn.Module:
    """
    Build the ResNet18 model architecture.
    """
    model = torchvision.models.resnet18(
        weights=torchvision.models.ResNet18_Weights.DEFAULT
    )
    model.fc = torch.nn.Linear(512, num_classes)
    return model