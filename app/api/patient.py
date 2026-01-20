from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.patient import Patient
from app.schemas.patient import PatientCreateSchema, PatientResponseSchema

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post(
    "", response_model=PatientResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_patient(payload: PatientCreateSchema, db: Session = Depends(get_db)):
    patient = Patient(
        full_name=payload.full_name,
        document=payload.document,
        birth_date=payload.birth_date,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("", response_model=list[PatientResponseSchema])
def list_patients(db: Session = Depends(get_db)):
    result = db.execute(select(Patient).order_by(Patient.id))
    return result.scalars().all()


@router.get("/{patient_id}", response_model=PatientResponseSchema)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
