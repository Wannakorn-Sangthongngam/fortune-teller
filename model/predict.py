import json
from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms

from model import TarotClassifier


MEAN = [0.485, 0.456, 0.406]
STD  = [0.229, 0.224, 0.225]

TRANSFORM = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(MEAN, STD),
])

CHECKPOINTS_DIR = Path("../checkpoints")


class TarotPredictor:
    def __init__(self, checkpoint_dir: str = str(CHECKPOINTS_DIR), device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # Load class names
        with open(Path(checkpoint_dir) / "classes.json") as f:
            self.classes: list[str] = json.load(f)

        # Load model
        self.model = TarotClassifier(num_classes=len(self.classes))
        self.model.load_state_dict(
            torch.load(Path(checkpoint_dir) / "best_model.pt", map_location=self.device)
        )
        self.model.to(self.device)
        self.model.eval()

    def predict(self, image_path: str, top_k: int = 3) -> list[dict]:
        """
        Returns top-k predictions as a list of dicts:
            [{"card": "00_fool", "confidence": 0.97}, ...]
        """
        image = Image.open(image_path).convert("RGB")
        tensor = TRANSFORM(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probs  = torch.softmax(logits, dim=1)[0]

        top_probs, top_idxs = probs.topk(top_k)
        return [
            {"card": self.classes[idx], "confidence": round(prob.item(), 4)}
            for prob, idx in zip(top_probs, top_idxs)
        ]

    def predict_from_pil(self, image: Image.Image, top_k: int = 3) -> list[dict]:
        """Same as predict() but accepts a PIL image directly."""
        tensor = TRANSFORM(image.convert("RGB")).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(tensor)
            probs  = torch.softmax(logits, dim=1)[0]

        top_probs, top_idxs = probs.topk(top_k)
        return [
            {"card": self.classes[idx], "confidence": round(prob.item(), 4)}
            for prob, idx in zip(top_probs, top_idxs)
        ]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path>")
        sys.exit(1)

    predictor = TarotPredictor()
    results = predictor.predict(sys.argv[1])
    for r in results:
        print(f"  {r['card']:30s}  {r['confidence']*100:.1f}%")
