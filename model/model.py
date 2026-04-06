import torch
import torch.nn as nn
from torchvision import models


class TarotClassifier(nn.Module):
    def __init__(self, num_classes: int = 78, dropout: float = 0.3):
        super().__init__()

        # Load pretrained EfficientNet-B0
        self.backbone = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)

        # Replace the classifier head
        in_features = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(p=dropout),
            nn.Linear(512, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)

    def freeze_backbone(self):
        """Freeze all backbone layers except the classifier head."""
        for param in self.backbone.features.parameters():
            param.requires_grad = False

    def unfreeze_backbone(self):
        """Unfreeze all backbone layers for fine-tuning."""
        for param in self.backbone.features.parameters():
            param.requires_grad = True


def build_model(num_classes: int = 78, freeze: bool = True) -> TarotClassifier:
    model = TarotClassifier(num_classes=num_classes)
    if freeze:
        model.freeze_backbone()
    return model
