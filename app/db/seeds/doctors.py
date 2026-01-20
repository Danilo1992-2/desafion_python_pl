from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.models.care_unit import CareUnit

DEFAULT_DOCTORS = [
    {
        "full_name": "Dra. Ana Lima",
        "crm": "CRM-SP-123456",
        "specialty": "Clínico Geral",
    },
    {"full_name": "Dr. Bruno Souza", "crm": "CRM-SP-654321", "specialty": "Pediatria"},
]


def seed_doctors(db: Session) -> None:
    for d in DEFAULT_DOCTORS:
        exists = db.scalar(select(Doctor.id).where(Doctor.crm == d["crm"]))
        if exists:
            continue

        db.add(
            Doctor(full_name=d["full_name"], crm=d["crm"], specialty=d.get("specialty"))
        )

    db.commit()
