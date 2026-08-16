# ML Model — Risk Prediction & Triage

## Goal
Predict patient risk level (Critical / Urgent / Stable) from vitals + symptoms, and explain *why* using SHAP.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install scikit-learn pandas shap fastapi uvicorn
```

## Files
- `train_model.py` — trains the risk classification model on sample data
- `predict_api.py` — exposes the model as an API for the backend to call

## Next Steps
1. Replace `data/sample_patients.csv` with a real triage dataset (e.g. Kaggle "ESI triage" dataset)
2. Train baseline model (`train_model.py`)
3. Add SHAP explainability
4. Wrap in FastAPI (`predict_api.py`) so backend can call `/predict`
