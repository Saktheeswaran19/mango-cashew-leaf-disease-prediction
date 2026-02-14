import os
import json
import numpy as np
from tensorflow.keras.models import load_model



MODEL_PATH = "./models/best_model.h5"
CLASS_MAP_PATH = "./models/class_map.json"   # folder that contains subfolders per class
IMG_SIZE = 224
BATCH_SIZE = 32



model = load_model(MODEL_PATH)
print(model.summary())
print("Last layer activation:", model.layers[-1].activation.__name__)