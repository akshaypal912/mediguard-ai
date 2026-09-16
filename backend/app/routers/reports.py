from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Patient, RiskAssessment
from ..schemas import ReportOut

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/patient/{patient_id}", response_model=ReportOut)
def patient_report(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")

    r = (
        db.query(RiskAssessment)
        .filter(RiskAssessment.patient_id == patient_id)
        .order_by(RiskAssessment.id.desc())
        .first()
    )

    latest = None
    if r:
        latest = {
            "id": r.id,
            "patient_id": r.patient_id,
            "risk_level": r.risk_level,
            "risk_score": r.risk_score,
            "probability": r.probability,
            "explanation": r.explanation,
            "recommendations": r.recommendations.split("||") if r.recommendations else [],
            "created_at": r.created_at,
        }

    return {
        "patient": patient,
        "latest_assessment": latest,
        "generated_at": datetime.utcnow(),
    }
