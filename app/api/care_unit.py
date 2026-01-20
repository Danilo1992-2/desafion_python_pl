from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.care_unit import CareUnit
from app.schemas.care_unit import CareUnitCreateSchema, CareUnitResponseSchema

router = APIRouter(prefix="/care-units", tags=["care_units"])


@router.post(
    "", response_model=CareUnitResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_care_unit(payload: CareUnitCreateSchema, db: Session = Depends(get_db)):
    unit = CareUnit(
        name=payload.name,
        cnes=payload.cnes,
        city=payload.city,
        state=payload.state,
    )
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


@router.get("", response_model=list[CareUnitResponseSchema])
def list_care_units(db: Session = Depends(get_db)):
    result = db.execute(select(CareUnit).order_by(CareUnit.id))
    return result.scalars().all()


@router.get("/{care_unit_id}", response_model=CareUnitResponseSchema)
def get_care_unit(care_unit_id: int, db: Session = Depends(get_db)):
    unit = db.get(CareUnit, care_unit_id)
    if not unit:
        raise HTTPException(status_code=404, detail="Care unit not found")
    return unit
