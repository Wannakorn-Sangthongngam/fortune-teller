# Fortune Teller Tarot Card Predictor

This program uses machine learning to recognize tarot cards from photos and provide fortune predictions.

## Setup

1. Install dependencies: The virtual environment is set up, and packages are installed.

2. Collect Data:
   - Take photos of each tarot card.
   - Organize in `data/train/` and `data/val/` with subfolders for each card (e.g., `data/train/The_Fool/`, `data/train/The_Magician/`).
   - Aim for 50-100 images per card for training.

3. Train the Model:
   - Run `python src/train.py` from the project root.
   - This will train a CNN model using transfer learning with MobileNetV2.

4. Predict:
   - Run `python src/predict.py` to capture from webcam and get predictions.

## Architecture

- **Model**: MobileNetV2 (pre-trained on ImageNet) with custom classification head.
- **Input**: 224x224 RGB images.
- **Output**: Probability distribution over tarot card classes.
- **Training**: Fine-tuning with data augmentation.

## Training Process

1. Data preprocessing: Resize, normalize, augment.
2. Transfer learning: Freeze base layers, train top layers.
3. Fine-tune: Unfreeze some layers if needed for better accuracy.
4. Evaluate on validation set.

## Notes

- Expand the `fortunes` dictionary in `predict.py` with actual tarot meanings.
- For better accuracy, collect more diverse images (different lighting, angles).
- If using GPU, TensorFlow will use it automatically.