from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.care_unit import CareUnit

DEFAULT_CARE_UNITS = [
    {"name": "Hospital Central", "city": "São Paulo", "state": "SP"},
    {"name": "UPA Zona Sul", "city": "São Paulo", "state": "SP"},
]


def seed_care_units(db: Session) -> None:
    for cu in DEFAULT_CARE_UNITS:
        exists = db.scalar(
            select(CareUnit.id).where(
                CareUnit.name == cu["name"],
                CareUnit.city == cu["city"],
                CareUnit.state == cu["state"],
            )
        )
        if exists:
            continue
        db.add(CareUnit(**cu))

    db.commit()
