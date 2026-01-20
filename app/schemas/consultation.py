from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ConsultationCreateSchema(BaseModel):
    patient_id: int = Field(..., description="Patient ID")
    doctor_id: int = Field(..., description="Doctor ID")
    care_unit_id: int = Field(..., description="Care unit (hospital) ID")
    symptoms: str = Field(..., description="Symptoms reported by the patient")
    patient_notes: Optional[str] = Field(
        None, description="Notes written by the patient"
    )
    medical_notes: Optional[str] = Field(
        None, description="Notes written by the doctor"
    )
    appointment_datetime: datetime = Field(..., description="Appointment date and time")


class ConsultationResponseSchema(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    symptoms: str
    patient_notes: Optional[str] = None
    medical_notes: Optional[str] = None
    appointment_datetime: datetime

    model_config = ConfigDict(from_attributes=True)


class ConsultationSummaryResponse(BaseModel):
    consultation_id: int = Field(..., description="Consultation ID")
    patient_name: str = Field(..., description="Patient full name")
    doctor_name: str = Field(..., description="Doctor full name")
    summary: str = Field(..., description="Structured clinical summary")
    strategy: str = Field(..., description="rule_based or llm_based")
    created_at: datetime = Field(..., description="When the summary was generated")
