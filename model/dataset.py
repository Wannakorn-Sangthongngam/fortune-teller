from pathlib import Path
from typing import Tuple

from PIL import Image
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms


# ImageNet normalization (used by EfficientNet pretrained weights)
MEAN = [0.485, 0.456, 0.406]
STD  = [0.229, 0.224, 0.225]


def get_transforms(train: bool = True) -> transforms.Compose:
    if train:
        return transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(MEAN, STD),
        ])
    else:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(MEAN, STD),
        ])


class TarotDataset(Dataset):
    """
    Expects data/ folder structure:
        data/raw/
            00_fool/
                img1.jpg
                img2.jpg
            01_magician/
                ...
    """

    def __init__(self, root: str, train: bool = True):
        self.root = Path(root)
        self.transform = get_transforms(train)

        # Each subfolder = one class
        class_dirs = sorted([d for d in self.root.iterdir() if d.is_dir()])
        self.classes = [d.name for d in class_dirs]
        self.class_to_idx = {c: i for i, c in enumerate(self.classes)}

        self.samples: list[Tuple[Path, int]] = []
        for d in class_dirs:
            label = self.class_to_idx[d.name]
            for img_path in d.iterdir():
                if img_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                    self.samples.append((img_path, label))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int):
        path, label = self.samples[idx]
        image = Image.open(path).convert("RGB")
        return self.transform(image), label


def build_dataloaders(
    data_dir: str,
    batch_size: int = 32,
    val_split: float = 0.15,
    test_split: float = 0.10,
    num_workers: int = 2,
):
    full_dataset = TarotDataset(data_dir, train=True)
    n = len(full_dataset)
    n_val  = int(n * val_split)
    n_test = int(n * test_split)
    n_train = n - n_val - n_test

    train_ds, val_ds, test_ds = random_split(full_dataset, [n_train, n_val, n_test])

    # Override transforms for val/test (no augmentation)
    val_ds.dataset  = TarotDataset(data_dir, train=False)
    test_ds.dataset = TarotDataset(data_dir, train=False)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,  num_workers=num_workers)
    val_loader   = DataLoader(val_ds,   batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader  = DataLoader(test_ds,  batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return train_loader, val_loader, test_loader, full_dataset.classes
