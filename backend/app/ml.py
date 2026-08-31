from pathlib import Path
import joblib
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = BASE_DIR.parent / "data" / "models" / "risk_model.joblib"

FEATURES = ["age", "heart_rate", "spo2", "systolic_bp", "respiratory_rate"]

_model = None

def load_model():
    global _model
    if MODEL_PATH.exists():
        try:
            _model = joblib.load(MODEL_PATH)
        except Exception:
            _model = None
    return _model

def predict_risk(age: int, heart_rate: float, spo2: float,
                 systolic_bp: float, respiratory_rate: float) -> dict:
    model = _model or load_model()
    x = np.array([[age, heart_rate, spo2, systolic_bp, respiratory_rate]], dtype=float)

    if model is not None:
        pred = int(model.predict(x)[0])
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(x)[0]
            probability = float(max(probs))
        else:
            probability = 0.75
        labels = {0: "Stable", 1: "Urgent", 2: "Critical"}
        level = labels.get(pred, "Urgent")
        return {"level": level, "probability": round(probability, 4), "source": "ml_model"}

    # Safe fallback for demo when no trained model exists.
    score = 0.0
    if spo2 < 92: score += 35
    elif spo2 < 95: score += 18
    if systolic_bp >= 180 or systolic_bp < 90: score += 25
    elif systolic_bp >= 140: score += 12
    if heart_rate >= 120 or heart_rate < 50: score += 20
    elif heart_rate >= 100: score += 8
    if respiratory_rate >= 30 or respiratory_rate < 8: score += 20
    elif respiratory_rate >= 22: score += 8

    score = min(score, 100)
    if score >= 60:
        level = "Critical"
    elif score >= 30:
        level = "Urgent"
    else:
        level = "Stable"

    probability = score / 100.0
    return {"level": level, "probability": round(probability, 4), "source": "clinical-rule-fallback"}
