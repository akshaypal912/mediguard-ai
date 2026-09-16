from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Patient, RiskAssessment
from ..schemas import AssessmentRequest, AssessmentOut
from ..ml import predict_risk
from ..risk_engine import analyze

router = APIRouter(prefix="/api/assessments", tags=["Risk Assessment"])

@router.post("", response_model=AssessmentOut, status_code=201)
def create_assessment(payload: AssessmentRequest, db: Session = Depends(get_db)):
    patient = db.get(Patient, payload.patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")

    result = predict_risk(
        patient.age,
        payload.heart_rate,
        payload.spo2,
        payload.systolic_bp,
        payload.respiratory_rate,
    )
    explanation = analyze(
        patient.age,
        payload.heart_rate,
        payload.spo2,
        payload.systolic_bp,
        payload.respiratory_rate,
        result["level"],
    )

    assessment = RiskAssessment(
        patient_id=patient.id,
        heart_rate=payload.heart_rate,
        spo2=payload.spo2,
        systolic_bp=payload.systolic_bp,
        respiratory_rate=payload.respiratory_rate,
        risk_level=result["level"],
        risk_score=round(result["probability"] * 100, 2),
        probability=result["probability"],
        explanation=explanation["explanation"],
        recommendations="||".join(explanation["recommendations"]),
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return {
        "id": assessment.id,
        "patient_id": assessment.patient_id,
        "risk_level": assessment.risk_level,
        "risk_score": assessment.risk_score,
        "probability": assessment.probability,
        "explanation": assessment.explanation,
        "recommendations": explanation["recommendations"],
        "created_at": assessment.created_at,
    }

@router.get("/patient/{patient_id}", response_model=list[AssessmentOut])
def patient_assessments(patient_id: int, db: Session = Depends(get_db)):
    if not db.get(Patient, patient_id):
        raise HTTPException(404, "Patient not found")
    rows = (
        db.query(RiskAssessment)
        .filter(RiskAssessment.patient_id == patient_id)
        .order_by(RiskAssessment.id.desc())
        .all()
    )
    return [{
        "id": r.id,
        "patient_id": r.patient_id,
        "risk_level": r.risk_level,
        "risk_score": r.risk_score,
        "probability": r.probability,
        "explanation": r.explanation,
        "recommendations": r.recommendations.split("||") if r.recommendations else [],
        "created_at": r.created_at,
    } for r in rows]

@router.get("/latest/{patient_id}", response_model=AssessmentOut)
def latest_assessment(patient_id: int, db: Session = Depends(get_db)):
    if not db.get(Patient, patient_id):
        raise HTTPException(404, "Patient not found")
    r = (
        db.query(RiskAssessment)
        .filter(RiskAssessment.patient_id == patient_id)
        .order_by(RiskAssessment.id.desc())
        .first()
    )
    if not r:
        raise HTTPException(404, "No assessment found")
    return {
        "id": r.id,
        "patient_id": r.patient_id,
        "risk_level": r.risk_level,
        "risk_score": r.risk_score,
        "probability": r.probability,
        "explanation": r.explanation,
        "recommendations": r.recommendations.split("||") if r.recommendations else [],
        "created_at": r.created_at,
    }
