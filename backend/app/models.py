from datetime import datetime
from sqlalchemy import String, Float, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[str] = mapped_column(String(30), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    medical_history: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    assessments = relationship("RiskAssessment", back_populates="patient", cascade="all, delete-orphan")

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)

    heart_rate: Mapped[float] = mapped_column(Float, nullable=False)
    spo2: Mapped[float] = mapped_column(Float, nullable=False)
    systolic_bp: Mapped[float] = mapped_column(Float, nullable=False)
    respiratory_rate: Mapped[float] = mapped_column(Float, nullable=False)

    risk_level: Mapped[str] = mapped_column(String(30), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    probability: Mapped[float] = mapped_column(Float, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    recommendations: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="assessments")

class MedicationCheck(Base):
    __tablename__ = "medication_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False, index=True)
    medications: Mapped[str] = mapped_column(Text, nullable=False)
    warning: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
