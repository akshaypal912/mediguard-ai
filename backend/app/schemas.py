from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class PatientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    age: int = Field(ge=0, le=120)
    gender: str = Field(min_length=1, max_length=30)
    phone: str | None = None
    medical_history: str | None = None

class PatientOut(PatientCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AssessmentRequest(BaseModel):
    patient_id: int
    heart_rate: float = Field(gt=0, le=250)
    spo2: float = Field(gt=0, le=100)
    systolic_bp: float = Field(gt=0, le=300)
    respiratory_rate: float = Field(gt=0, le=100)

class AssessmentOut(BaseModel):
    id: int
    patient_id: int
    risk_level: str
    risk_score: float
    probability: float
    explanation: str
    recommendations: list[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MedicationRequest(BaseModel):
    patient_id: int
    medications: list[str] = Field(min_length=1)

class MedicationOut(BaseModel):
    id: int
    patient_id: int
    medications: list[str]
    warning: str
    severity: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReportOut(BaseModel):
    patient: PatientOut
    latest_assessment: AssessmentOut | None
    generated_at: datetime
