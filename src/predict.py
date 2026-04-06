import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import os

# Load model
model_path = '../models/tarot_model.h5'
model = load_model(model_path)

# Class names (assuming same as folder names)
data_dir = '../data/train'
class_names = sorted(os.listdir(data_dir))

# Fortunes dictionary (sample, you can expand)
fortunes = {
    'The Fool': 'New beginnings await you.',
    'The Magician': 'You have the power to manifest your desires.',
    # Add more...
}

def predict_card(image_path):
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions)
    card_name = class_names[class_idx]
    return card_name

def capture_and_predict():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    print("Press 'c' to capture image, 'q' to quit")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Tarot Card Capture', frame)
        key = cv2.waitKey(1)
        if key == ord('c'):
            img_path = 'captured_card.jpg'
            cv2.imwrite(img_path, frame)
            card = predict_card(img_path)
            fortune = fortunes.get(card, 'Mysterious forces at play.')
            print(f"Predicted Card: {card}")
            print(f"Fortune: {fortune}")
            cv2.imshow('Captured', frame)
            cv2.waitKey(0)
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_predict()