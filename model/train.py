import json
from pathlib import Path

import torch
import torch.nn as nn
from torch.optim import Adam
from torch.optim.lr_scheduler import CosineAnnealingLR
from tqdm import tqdm

from dataset import build_dataloaders
from model import build_model


# ── Config ────────────────────────────────────────────────────────────────────
DATA_DIR    = "../data/raw"
SAVE_DIR    = Path("../checkpoints")
BATCH_SIZE  = 32
PHASE1_EPOCHS = 10   # backbone frozen
PHASE2_EPOCHS = 20   # backbone unfrozen (fine-tune)
LR_PHASE1   = 1e-3
LR_PHASE2   = 1e-4
DEVICE      = "cuda" if torch.cuda.is_available() else "cpu"
# ──────────────────────────────────────────────────────────────────────────────


def accuracy(outputs: torch.Tensor, labels: torch.Tensor) -> float:
    preds = outputs.argmax(dim=1)
    return (preds == labels).float().mean().item()


def run_epoch(model, loader, criterion, optimizer, train: bool):
    model.train() if train else model.eval()
    total_loss, total_acc = 0.0, 0.0

    ctx = torch.enable_grad() if train else torch.no_grad()
    with ctx:
        for images, labels in tqdm(loader, leave=False):
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            loss = criterion(outputs, labels)

            if train:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            total_loss += loss.item()
            total_acc  += accuracy(outputs, labels)

    n = len(loader)
    return total_loss / n, total_acc / n


def train(data_dir: str = DATA_DIR):
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    train_loader, val_loader, test_loader, classes = build_dataloaders(
        data_dir, batch_size=BATCH_SIZE
    )
    num_classes = len(classes)
    print(f"Classes: {num_classes}  |  Device: {DEVICE}")

    # Save class index mapping
    with open(SAVE_DIR / "classes.json", "w") as f:
        json.dump(classes, f, indent=2)

    model = build_model(num_classes=num_classes, freeze=True).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    best_val_acc = 0.0

    # ── Phase 1: Train head only ──────────────────────────────────────────────
    print("\n=== Phase 1: Training classifier head (backbone frozen) ===")
    optimizer = Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=LR_PHASE1)
    scheduler = CosineAnnealingLR(optimizer, T_max=PHASE1_EPOCHS)

    for epoch in range(1, PHASE1_EPOCHS + 1):
        train_loss, train_acc = run_epoch(model, train_loader, criterion, optimizer, train=True)
        val_loss,   val_acc   = run_epoch(model, val_loader,   criterion, optimizer, train=False)
        scheduler.step()

        print(f"[P1 {epoch:02d}/{PHASE1_EPOCHS}] "
              f"train_loss={train_loss:.4f} train_acc={train_acc:.3f} | "
              f"val_loss={val_loss:.4f} val_acc={val_acc:.3f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), SAVE_DIR / "best_model.pt")
            print(f"  ✓ Saved best model (val_acc={val_acc:.3f})")

    # ── Phase 2: Fine-tune full model ─────────────────────────────────────────
    print("\n=== Phase 2: Fine-tuning full model (backbone unfrozen) ===")
    model.unfreeze_backbone()
    optimizer = Adam(model.parameters(), lr=LR_PHASE2, weight_decay=1e-4)
    scheduler = CosineAnnealingLR(optimizer, T_max=PHASE2_EPOCHS)

    for epoch in range(1, PHASE2_EPOCHS + 1):
        train_loss, train_acc = run_epoch(model, train_loader, criterion, optimizer, train=True)
        val_loss,   val_acc   = run_epoch(model, val_loader,   criterion, optimizer, train=False)
        scheduler.step()

        print(f"[P2 {epoch:02d}/{PHASE2_EPOCHS}] "
              f"train_loss={train_loss:.4f} train_acc={train_acc:.3f} | "
              f"val_loss={val_loss:.4f} val_acc={val_acc:.3f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), SAVE_DIR / "best_model.pt")
            print(f"  ✓ Saved best model (val_acc={val_acc:.3f})")

    # ── Final test evaluation ─────────────────────────────────────────────────
    print("\n=== Test Evaluation ===")
    model.load_state_dict(torch.load(SAVE_DIR / "best_model.pt"))
    test_loss, test_acc = run_epoch(model, test_loader, criterion, None, train=False)
    print(f"Test Loss: {test_loss:.4f}  |  Test Accuracy: {test_acc:.3f}")


if __name__ == "__main__":
    train()
