# backend/server.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
import io
import numpy as np
import asyncio

app = FastAPI(title="Mango Leaf Disease Detector - Inference API")

# Allow dev origin (Vite default). Add production origins later.
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
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


# -- Model loading placeholder --
# Implement actual model loading here (load once at startup).
MODEL = None


def load_model():
    """
    Replace this stub with code to load your trained model (Torch, TF, ONNX...), e.g.:
      - torch.load(...)
      - keras.models.load_model(...)
      - onnxruntime.InferenceSession(...)
    Return the loaded model object.
    """
    # For now return None (mock). Replace with real model.
    return None


@app.on_event("startup")
async def startup_event():
    global MODEL
    MODEL = load_model()
    # If model loading is synchronous and heavy, consider running in threadpool
    # e.g. MODEL = await asyncio.to_thread(load_model)


# -- Helper to read image bytes into PIL Image --
def read_image_from_uploadfile(upload_file: UploadFile) -> Image.Image:
    contents = upload_file.file.read()
    upload_file.file.seek(0)
    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")
    return image


# -- Inference function placeholder --
def run_model_inference(image: Image.Image) -> AnalyzeResult:
    """
    Replace this with code that:
      - Preprocesses `image` into model input (resize, normalize, to array/tensor)
      - Runs model inference
      - Maps model outputs to the expected JSON structure
    For now, returns a mock/dummy AnalyzeResult to match front-end expectations.
    """
    # Example of a mock response — replace with real results
    return AnalyzeResult(
        name="Anthracnose",
        confidence=0.89,
        severity="moderate",
        description="Anthracnose is a fungal disease that causes dark lesions on leaves and fruit. It typically appears during warm, humid weather conditions.",
        recommendations=[
            "Remove and destroy infected leaves immediately",
            "Apply copper-based fungicide every 10-14 days",
            "Improve air circulation around trees",
            "Avoid overhead watering to reduce leaf wetness",
            "Consider using resistant mango varieties for future planting",
        ],
    )


# -- POST /api/analyze endpoint --
@app.post("/api/analyze", response_model=AnalyzeResult)
async def analyze(image: UploadFile = File(...)):
    """
    Expects multipart/form-data with a single file field named 'image'.
    Example from frontend:
      formData.append('image', selectedFile)
    """
    # Basic validation
    if not image:
        raise HTTPException(status_code=400, detail="Missing image file")

    # Validate content-type (optional)
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    # Read image (blocking IO) — if heavy, run in threadpool
    try:
        # Because UploadFile.file.read() is blocking, run in thread
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read image: {e}")

    # Call model inference (if heavy / uses CPU/GPU, run in threadpool)
    try:
        # If MODEL is None (not yet implemented), the run_model_inference returns a mock
        if MODEL is None:
            result = await asyncio.to_thread(run_model_inference, img)
        else:
            # Example: run synchronous inference in thread
            result = await asyncio.to_thread(run_model_inference, img)
            # Or if you implement async model inference, call it directly.
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")
    
    print(
    "Received:",
    image.filename,
    "size:",
    len(contents),
    "type:",
    image.content_type)

    return result


# Optional health check
@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": MODEL is not None}

