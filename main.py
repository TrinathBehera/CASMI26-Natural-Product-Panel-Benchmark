import os
import pickle
import traceback
from pathlib import Path

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="CASMI 2016 Natural Product Identifier")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "model.pkl"
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Match the model's trained feature set exactly. Missing values are filled with 0.0 to keep
# older clients and partial payloads from crashing the prediction call.
class CandidateInput(BaseModel):
    rank: float = 0.0
    ranker_score: float = 0.0
    pool_row: float = 0.0
    popularity: float = 0.0
    pool_source: float = 0.0
    lib_max: float = 0.0

@app.post("/predict")
def predict(data: CandidateInput):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded.")

    try:
        feature_names = list(getattr(model, "feature_names_in_", []))
        input_dict = data.model_dump()

        if feature_names:
            for feature in feature_names:
                input_dict.setdefault(feature, 0.0)
            input_df = pd.DataFrame([input_dict], columns=feature_names)
        else:
            input_df = pd.DataFrame([input_dict])

        prediction = model.predict(input_df)[0]

        probability = None
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            if len(probabilities) > 1:
                probability = float(probabilities[1])

        return {
            "is_truth": int(prediction),
            "confidence": probability
        }

    except Exception as e:
        print("\n================ ERROR TRACEBACK ================")
        traceback.print_exc()
        print("=================================================\n")
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
