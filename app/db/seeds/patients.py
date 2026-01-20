from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.patient import Patient

DEFAULT_PATIENTS = [
    {
        "full_name": "Carlos Silva",
        "document": "11122233344",
        "birth_date": "1990-05-10",
    },
    {
        "full_name": "Mariana Alves",
        "document": "55566677788",
        "birth_date": "1985-11-02",
    },
]


def seed_patients(db: Session) -> None:
    for p in DEFAULT_PATIENTS:
        exists = db.scalar(select(Patient.id).where(Patient.document == p["document"]))
        if exists:
            continue

        db.add(Patient(**p))

    db.commit()
