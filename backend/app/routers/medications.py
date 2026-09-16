from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Patient, MedicationCheck
from ..schemas import MedicationRequest, MedicationOut

router = APIRouter(prefix="/api/medications", tags=["Medication Safety"])

KNOWN_CONFLICTS = [
    ({"warfarin", "aspirin"}, "Potential bleeding-risk combination. Verify with a qualified clinician.", "High"),
    ({"ibuprofen", "warfarin"}, "Potential bleeding-risk interaction. Verify with a qualified clinician.", "High"),
    ({"metformin", "alcohol"}, "Potential safety concern. Review with a qualified clinician.", "Moderate"),
]

@router.post("/check", response_model=MedicationOut, status_code=201)
def check_medications(payload: MedicationRequest, db: Session = Depends(get_db)):
    if not db.get(Patient, payload.patient_id):
        raise HTTPException(404, "Patient not found")

    meds = {m.strip().lower() for m in payload.medications if m.strip()}
    warning = "No known conflict detected by the demo rule set. This is not a substitute for a pharmacist/doctor review."
    severity = "Low"

    for pair, message, level in KNOWN_CONFLICTS:
        if pair.issubset(meds):
            warning, severity = message, level
            break

    row = MedicationCheck(
        patient_id=payload.patient_id,
        medications="||".join(sorted(meds)),
        warning=warning,
        severity=severity,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "id": row.id,
        "patient_id": row.patient_id,
        "medications": sorted(meds),
        "warning": row.warning,
        "severity": row.severity,
        "created_at": row.created_at,
    }
