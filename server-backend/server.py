# backend/server.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict 
from PIL import Image
import io
import numpy as np
import asyncio
from model import predict_mango, predict_cashew

app = FastAPI(title="Mango Leaf Disease Detector - Inference API")




MANGO_DISEASE_INFO = {
    "Anthracnose": {
        "severity": "moderate",
        "description": "Anthracnose is a fungal disease that causes dark, sunken lesions on young leaves and fruit. Symptoms include brown to black spots that may coalesce and form larger patches.",
        "recommendations": [
            "Remove and destroy infected leaves and fruits to reduce inoculum.",
            "Apply a copper-based fungicide or recommended systemic fungicide according to label instructions.",
            "Ensure good air circulation by pruning and avoid overhead irrigation.",
            "Treat young trees earlier in the season when conditions are wet."
        ]
    },
    "Bacterial Canker": {
        "severity": "moderate",
        "description": "Bacterial canker causes lesions and cankers on twigs and fruit; often results from wounds and spread in wet conditions.",
        "recommendations": [
            "Prune and remove infected twigs; disinfect pruning tools.",
            "Avoid wounding trees during high-risk seasons.",
            "Apply appropriate bactericides if recommended in your region."
        ]
    },
    "Cutting Weevil": {
        "severity": "mild",
        "description": "Cutting weevil causes feeding damage to leaves and may stunt growth. Look for small holes and feeding marks.",
        "recommendations": [
            "Handpick adults where practical and use pheromone traps.",
            "Use approved insecticides when infestations are high.",
            "Maintain tree vigor via proper nutrition to tolerate pest pressure."
        ]
    },
    "Die Back": {
        "severity": "severe",
        "description": "Die back causes progressive death of shoots and branches. It can be caused by fungi or environmental stress.",
        "recommendations": [
            "Remove dead branches and improve tree health (watering, fertilization).",
            "Apply fungicidal treatments if a fungal pathogen is confirmed.",
            "Consult local extension for diagnosis and targeted control."
        ]
    },
    "Gall Midge": {
        "severity": "mild",
        "description": "Gall midge infestation results in galls and distorted growth on leaves or shoots. Reduces yield if severe.",
        "recommendations": [
            "Monitor for gall formation and prune affected parts.",
            "Use biological control where available and approved insecticides as needed."
        ]
    },
    "Healthy": {
        "severity": "healthy",
        "description": "No disease detected. Your tree appears healthy. Continue good cultural practices to keep it healthy.",
        "recommendations": [
            "Maintain regular irrigation and balanced fertilization.",
            "Monitor routinely for pests and diseases."
        ]
    },
    "Powdery Mildew": {
        "severity": "moderate",
        "description": "Powdery mildew presents as white powdery fungal growth on leaf surfaces and young shoots.",
        "recommendations": [
            "Improve air flow and reduce humidity around the canopy.",
            "Apply sulfur or other fungicides labeled for powdery mildew."
        ]
    },
    "Sooty Mould": {
        "severity": "mild",
        "description": "Sooty mould grows on honeydew excreted by sap-sucking insects and causes dark coating on leaves, reducing photosynthesis.",
        "recommendations": [
            "Control sap-sucking insects (aphids, scales) that produce honeydew.",
            "Wash leaves to remove persistent sooty mold when practical."
        ]
    }
}

# -------------------------------------------------------------------
# CASHEW DISEASE INFO
# -------------------------------------------------------------------

CASHEW_DISEASE_INFO = {
    "Anthracnose": {
        "severity": "moderate",
        "description": "Cashew anthracnose causes dark lesions on leaves and nuts.",
        "recommendations": [
            "Remove infected parts.",
            "Apply copper-based fungicides.",
            "Avoid overhead irrigation."
        ]
    },
    "Gray Blight": {
        "severity": "moderate",
        "description": "Gray blight causes grayish necrotic leaf spots in cashew plants.",
        "recommendations": [
            "Remove affected leaves.",
            "Spray recommended fungicides."
        ]
    },
    "Red Rust": {
        "severity": "mild",
        "description": "Red rust appears as orange-red patches on cashew leaves.",
        "recommendations": [
            "Improve canopy ventilation.",
            "Apply copper fungicide if severe."
        ]
    },
    "Healthy": {
        "severity": "healthy",
        "description": "No disease detected. Cashew plant appears healthy.",
        "recommendations": [
            "Maintain nutrient balance.",
            "Monitor periodically."
        ]
    }
}

def normalize_prediction(raw: Dict, disease_info: Dict) -> Dict:
    r = raw.copy() if isinstance(raw, dict) else {}

    name = r.get("name", "Unknown")

    try:
        confidence = float(r.get("confidence", 0.0))
    except Exception:
        confidence = 0.0

    # Convert probabilities to %
    all_probs = r.get("all_probs", {})
    all_probabilities = {
        k: float(v) * 100 for k, v in all_probs.items()
    } if isinstance(all_probs, dict) else {}

    severity = None
    description = None
    recommendations = []

    info = disease_info.get(name)
    if info:
        severity = info.get("severity")
        description = info.get("description")
        recommendations = info.get("recommendations", [])

    return {
        "name": name,
        "confidence": confidence * 100,
        "severity": severity,
        "description": description,
        "recommendations": recommendations,
        "all_probabilities": all_probabilities
    }

# Allow dev origin (Vite default). Add production origins later.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://192.168.1.11:8000"
    # add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response model the frontend expects
class AnalyzeResult(BaseModel):
    name: str
    confidence: float
    severity: Optional[str] = None
    description: Optional[str] = None
    recommendations: Optional[List[str]] = None
    all_probabilities: Optional[dict] = None


# -- POST /api/analyze endpoint --
@app.post("/api/analyze/mango", response_model=AnalyzeResult)
async def analyze_mango(image: UploadFile = File(...)):
    """
    Mango disease detection endpoint
    """

    # Basic validation
    if not image:
        raise HTTPException(status_code=400, detail="Missing image file")

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    # Read image
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read image: {e}")

    # Run Mango model inference
    try:
        raw_result = await asyncio.to_thread(predict_mango, img)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mango inference error: {e}")

    # Normalize result
    try:
        result_dict = normalize_prediction(raw_result, MANGO_DISEASE_INFO)
    except Exception as e:
        result_dict = {
            "name": "Unknown",
            "confidence": 0.0,
            "severity": None,
            "description": None,
            "recommendations": [],
            "all_probabilities": {}
        }
        print("normalize_prediction error (mango):", e)

    print(
        "[MANGO]",
        "Received:",
        image.filename,
        "type:",
        image.content_type,
        "-> Predicted:",
        result_dict.get("name"),
        "conf:",
        result_dict.get("confidence")
    )

    return result_dict

@app.post("/api/analyze/cashew", response_model=AnalyzeResult)
async def analyze_cashew(image: UploadFile = File(...)):
    """
    Cashew disease detection endpoint
    """

    # Basic validation
    if not image:
        raise HTTPException(status_code=400, detail="Missing image file")

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    # Read image
    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read image: {e}")

    # Run Cashew model inference
    try:
        raw_result = await asyncio.to_thread(predict_cashew, img)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cashew inference error: {e}")

    # Normalize result
    try:
        result_dict = normalize_prediction(raw_result, CASHEW_DISEASE_INFO)
    except Exception as e:
        result_dict = {
            "name": "Unknown",
            "confidence": 0.0,
            "severity": None,
            "description": None,
            "recommendations": [],
            "all_probabilities": {}
        }
        print("normalize_prediction error (cashew):", e)

    print(
        "[CASHEW]",
        "Received:",
        image.filename,
        "type:",
        image.content_type,
        "-> Predicted:",
        result_dict.get("name"),
        "conf:",
        result_dict.get("confidence")
    )

    return result_dict


# Optional health check
@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": "True"}



