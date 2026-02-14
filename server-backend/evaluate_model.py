import os
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# -------------------------
# Paths (adjust these)
# -------------------------
MODEL_PATH = "./models/mango_model.h5"
CLASS_MAP_PATH = "./models/class_map.json"
DATASET_DIR = "D:/mango-cashew/training/dataset"   # folder that contains subfolders per class
IMG_SIZE = 224
BATCH_SIZE = 32

# -------------------------
# Load model & classes
# -------------------------
model = load_model(MODEL_PATH)

with open(CLASS_MAP_PATH, "r") as f:
    class_names = json.load(f)

print("Loaded model and classes:")
print(class_names)

# -------------------------
# Create test generator
# -------------------------
datagen = ImageDataGenerator(rescale=1.0/255)

test_gen = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

# -------------------------
# Run prediction
# -------------------------
preds = model.predict(test_gen)
y_pred = np.argmax(preds, axis=1)
y_true = test_gen.classes

# -------------------------
# Accuracy
# -------------------------
acc = accuracy_score(y_true, y_pred)
print(f"\n🔥 MODEL ACCURACY: {acc*100:.2f}%\n")

# -------------------------
# Classification report
# -------------------------
print("📌 CLASSIFICATION REPORT")
print(classification_report(y_true, y_pred, target_names=class_names))

# -------------------------
# Confusion matrix
# -------------------------
print("📌 CONFUSION MATRIX")
print(confusion_matrix(y_true, y_pred))
