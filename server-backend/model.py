# backend/model.py

import json
import numpy as np
from typing import Dict, Any, List, Optional
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model

# ----------------------------------------------------------
# MODEL PATHS
# ----------------------------------------------------------

MANGO_MODEL_PATH = "models/mango_model.h5"
MANGO_CLASS_MAP_PATH = "models/mango_class_map.json"

CASHEW_MODEL_PATH = "models/cashew_model.h5"
CASHEW_CLASS_MAP_PATH = "models/cashew_class_map.json"

# ----------------------------------------------------------
# GPU CONFIGURATION
# ----------------------------------------------------------

gpus = tf.config.list_physical_devices("GPU")
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except Exception:
        pass

# ----------------------------------------------------------
# LOAD MODELS
# ----------------------------------------------------------

try:
    _MANGO_MODEL = load_model(MANGO_MODEL_PATH)
except Exception as e:
    _MANGO_MODEL = None
    _MANGO_ERROR = e
else:
    _MANGO_ERROR = None

try:
    _CASHEW_MODEL = load_model(CASHEW_MODEL_PATH)
except Exception as e:
    _CASHEW_MODEL = None
    _CASHEW_ERROR = e
else:
    _CASHEW_ERROR = None

# ----------------------------------------------------------
# LOAD CLASS MAPS
# ----------------------------------------------------------

try:
    with open(MANGO_CLASS_MAP_PATH, "r", encoding="utf-8") as f:
        MANGO_CLASS_NAMES: List[str] = json.load(f)
except Exception:
    MANGO_CLASS_NAMES = None

try:
    with open(CASHEW_CLASS_MAP_PATH, "r", encoding="utf-8") as f:
        CASHEW_CLASS_NAMES: List[str] = json.load(f)
except Exception:
    CASHEW_CLASS_NAMES = None

# ----------------------------------------------------------
# GET INPUT SIZE PER MODEL
# ----------------------------------------------------------

def _get_model_input_size(model: tf.keras.Model) -> (int, int):
    try:
        shape = model.input_shape
        if isinstance(shape, tuple) and len(shape) >= 3:
            h = shape[1] or 224
            w = shape[2] or 224
            return int(h), int(w)
    except Exception:
        pass
    return 224, 224

MANGO_IMG_H, MANGO_IMG_W = (
    _get_model_input_size(_MANGO_MODEL)
    if _MANGO_MODEL is not None else (224, 224)
)

CASHEW_IMG_H, CASHEW_IMG_W = (
    _get_model_input_size(_CASHEW_MODEL)
    if _CASHEW_MODEL is not None else (224, 224)
)

# ----------------------------------------------------------
# SAFETY CHECK
# ----------------------------------------------------------

def _ensure_model_loaded(model, error, model_name):
    if model is None:
        raise RuntimeError(f"{model_name} not loaded: {error!r}")

# ----------------------------------------------------------
# PREPROCESS FUNCTION
# ----------------------------------------------------------

def preprocess_image(image: Image.Image, target_size: tuple) -> np.ndarray:
    image = image.convert("RGB")
    image = image.resize((target_size[1], target_size[0]))  # (width, height)

    arr = np.array(image).astype(np.float32) / 255.0

    if arr.ndim == 2:
        arr = np.stack([arr] * 3, axis=-1)

    if arr.shape[-1] != 3:
        arr = arr[..., :3]

    arr = np.expand_dims(arr, axis=0)
    return arr

# ----------------------------------------------------------
# MANGO PREDICTION
# ----------------------------------------------------------

def predict_mango(image: Image.Image) -> Dict[str, Any]:
    _ensure_model_loaded(_MANGO_MODEL, _MANGO_ERROR, "Mango model")

    x = preprocess_image(image, (MANGO_IMG_H, MANGO_IMG_W))
    preds = _MANGO_MODEL.predict(x)[0]
    probs = np.asarray(preds).astype(float)

    idx = int(np.argmax(probs))
    confidence = float(probs[idx])

    label = MANGO_CLASS_NAMES[idx] if MANGO_CLASS_NAMES else str(idx)

    all_probs = {
        name: float(probs[i])
        for i, name in enumerate(MANGO_CLASS_NAMES)
    } if MANGO_CLASS_NAMES else {}

    return {
        "name": label,
        "confidence": confidence,
        "all_probs": all_probs
    }

# ----------------------------------------------------------
# CASHEW PREDICTION
# ----------------------------------------------------------

def predict_cashew(image: Image.Image) -> Dict[str, Any]:
    _ensure_model_loaded(_CASHEW_MODEL, _CASHEW_ERROR, "Cashew model")

    x = preprocess_image(image, (CASHEW_IMG_H, CASHEW_IMG_W))
    preds = _CASHEW_MODEL.predict(x)[0]
    probs = np.asarray(preds).astype(float)

    idx = int(np.argmax(probs))
    confidence = float(probs[idx])

    label = CASHEW_CLASS_NAMES[idx] if CASHEW_CLASS_NAMES else str(idx)

    all_probs = {
        name: float(probs[i])
        for i, name in enumerate(CASHEW_CLASS_NAMES)
    } if CASHEW_CLASS_NAMES else {}

    return {
        "name": label,
        "confidence": confidence,
        "all_probs": all_probs
    }
