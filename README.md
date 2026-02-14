🌿🍃 Multi-Crop Leaf Disease Detection System
<p align="center"> <b>AI-Powered Deep Learning Platform for Mango & Cashew Disease Classification</b><br/> Built with React + FastAPI + TensorFlow </p>
🚀 Project Overview

This project is a full-stack AI web application that detects plant leaf diseases using Deep Learning.

It supports:

🥭 Mango Leaf Disease Classification

🌰 Cashew Leaf Disease Classification

📊 Probability Distribution Visualization

📋 Severity Levels

💊 Treatment Recommendations

⚡ Real-time Inference

The system uses trained CNN models (.h5) with Softmax output to classify diseases and display confidence levels through an interactive bar chart.

🧠 Key Features

✨ Multi-crop support (Mango + Cashew)
✨ Separate AI models per crop
✨ Probability distribution bar chart
✨ Dynamic crop switching UI
✨ Crop-specific treatment advice
✨ Clean, responsive modern UI
✨ FastAPI async inference
✨ Scalable architecture

🏗️ Tech Stack
🎨 Frontend

React (TypeScript)

Vite

Tailwind CSS

shadcn/ui

Recharts

React Router DOM

TanStack React Query

⚙ Backend

FastAPI

TensorFlow / Keras

Pillow (PIL)

NumPy

AsyncIO

📂 Project Structure
leaf-snap-diagnosis/
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── pages/
│       │   ├── CropDetection.tsx
│       │   ├── Mango.tsx
│       │   ├── Cashew.tsx
│       │   ├── Index.tsx
│       │   └── NotFound.tsx
│       ├── App.tsx
│       └── main.tsx
│
├── server-backend/
│   ├── server.py
│   ├── model.py
│   └── models/
│       ├── mango_model.h5
│       ├── cashew_model.h5
│       ├── mango_class_map.json
│       └── cashew_class_map.json

🧪 Supported Diseases
🥭 Mango Diseases

Anthracnose

Bacterial Canker

Cutting Weevil

Die Back

Gall Midge

Powdery Mildew

Sooty Mould

Healthy

🌰 Cashew Diseases

Anthracnose

Gray Blight

Red Rust

Healthy

🔄 System Workflow
User selects crop →
Uploads image →
Frontend calls /api/analyze/{crop} →
Backend loads correct model →
Returns:
  - Predicted Disease
  - Confidence %
  - Full Probability Distribution
  - Severity Level
  - Description
  - Recommendations →
Frontend renders results + bar chart

📊 Probability Visualization

The model uses a Softmax output layer, allowing the system to:

Display top predicted disease

Show confidence percentage

Visualize full probability distribution via bar chart

Example:

Anthracnose → 82%
Powdery Mildew → 10%
Healthy → 5%
Others → 3%

🔌 API Endpoints
Method	Endpoint	Description
POST	/api/analyze/mango	Mango disease classification
POST	/api/analyze/cashew	Cashew disease classification
GET	/health	Server health check
▶️ How to Run the Project
1️⃣ Backend Setup
cd server-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn server:app --reload


Backend runs at:

http://127.0.0.1:8000

2️⃣ Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at:

http://localhost:5173

🖼️ UI Features

Modern gradient hero section

Crop toggle dropdown

Drag & drop image upload

Loading animation

Result cards

Interactive bar chart

Severity-based styling

📈 Model Architecture

Custom CNN Architecture

Input size dynamically determined

Softmax final layer

Batch normalization

Dropout regularization

Probability output mapping

🧩 Architecture Highlights

✔ Modular multi-model backend
✔ Reusable CropDetection component
✔ Clean routing (/mango, /cashew)
✔ Async non-blocking inference
✔ Crop-specific knowledge base

🔮 Future Improvements

Grad-CAM Visualization

Model Ensemble Comparison

Deployment (AWS / Render)

Image History Tracking

User Authentication

Database Integration

Mobile Optimization

📜 License

This project is for academic and research purposes.

👨‍💻 Author

Developed as a Deep Learning + Full Stack AI project
Demonstrating multi-crop disease classification using CNN models.

🌟 If you found this project useful, consider giving it a star!