from sqlalchemy.orm import Session

from app.db.seeds.symptoms import seed_symptoms
from app.db.seeds.care_units import seed_care_units
from app.db.seeds.doctors import seed_doctors
from app.db.seeds.patients import seed_patients


def run_seeds(db: Session) -> None:
    seed_symptoms(db)
    seed_care_units(db)
    seed_doctors(db)
    seed_patients(db)
