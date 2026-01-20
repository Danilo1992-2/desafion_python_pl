from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.models.symptom import Symptom
from app.schemas.symptom import SymptomCreateSchema, SymptomResponseSchema

router = APIRouter(prefix="/symptom", tags=["symptoms"])


@router.post(
    "", response_model=SymptomResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_symptom(payload: SymptomCreateSchema, db: Session = Depends(get_db)):
    symptom = Symptom(name=payload.name.strip(), description=payload.description)

    db.add(symptom)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Symptom already exists")

    db.refresh(symptom)
    return symptom


@router.get("", response_model=list[SymptomResponseSchema])
def list_symptoms(db: Session = Depends(get_db)):
    result = db.execute(select(Symptom).order_by(Symptom.name))
    return result.scalars().all()


@router.get("/{symptom_id}", response_model=SymptomResponseSchema)
def get_symptom(symptom_id: int, db: Session = Depends(get_db)):
    symptom = db.get(Symptom, symptom_id)
    if not symptom:
        raise HTTPException(status_code=404, detail="Symptom not found")
    return symptom
