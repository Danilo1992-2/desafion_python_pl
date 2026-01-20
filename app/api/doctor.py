from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreateSchema, DoctorResponseSchema

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.post(
    "", response_model=DoctorResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_doctor(payload: DoctorCreateSchema, db: Session = Depends(get_db)):
    doctor = Doctor(
        full_name=payload.full_name,
        crm=payload.crm,
        specialty=payload.specialty,
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.get("", response_model=list[DoctorResponseSchema])
def list_doctors(db: Session = Depends(get_db)):
    result = db.execute(select(Doctor).order_by(Doctor.id))
    return result.scalars().all()


@router.get("/{doctor_id}", response_model=DoctorResponseSchema)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
