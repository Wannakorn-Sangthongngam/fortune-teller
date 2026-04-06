# 🔮 Fortune Teller — Tarot Card AI

An AI-powered fortune teller that recognizes tarot cards from photos and generates predictions.

---

## Overview

Take a photo of a tarot card → AI identifies the card → Fortune is revealed.

---

## Roadmap

- [ ] **Phase 1: Data Collection** — Photograph all 78 tarot cards
- [ ] **Phase 2: Model Training** — Fine-tune EfficientNet-B0 on tarot card images
- [ ] **Phase 3: Prediction** — Identify card from photo with confidence score
- [ ] **Phase 4: Fortune Telling** — Map card to meaning and generate reading
- [ ] **Phase 5: App** — Build UI for the full experience

---

## Model Plan

- Architecture: EfficientNet-B0 (pretrained on ImageNet)
- Framework: PyTorch
- Classes: 78 (Major + Minor Arcana)
- Training: Transfer learning — 2 phase fine-tuning
- Platform: Google Colab (T4 GPU)

---

## Project Structure

```
fortune-teller/
├── model/
│   ├── model.py          # EfficientNetB0 classifier
│   ├── dataset.py        # Data loading + augmentation
│   ├── train.py          # Training loop
│   └── predict.py        # Inference
├── tarot_training.ipynb  # Google Colab notebook
└── requirements.txt
```

---

> Work in progress — details will be updated as the project develops.
