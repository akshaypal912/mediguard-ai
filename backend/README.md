# MediGuardAI Backend

FastAPI backend for patient management, AI risk assessment, medication safety checks, and reports.

## Run

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## API

- GET `/health`
- POST/GET `/api/patients`
- GET `/api/patients/{patient_id}`
- POST `/api/assessments`
- GET `/api/assessments/patient/{patient_id}`
- GET `/api/assessments/latest/{patient_id}`
- POST `/api/medications/check`
- GET `/api/reports/patient/{patient_id}`

The trained model is loaded from `data/models/risk_model.joblib` when available. If it is missing, the API uses a transparent demo fallback based on submitted vital signs.
