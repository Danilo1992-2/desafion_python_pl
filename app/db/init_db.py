from sqlalchemy.orm import Session

from app.db.session import engine
from app.db.base import Base

# Importa models pra registrar no metadata
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.consultation import Consultation
from app.models.care_unit import CareUnit
from app.models.symptom import Symptom

from app.db.seeds.run import run_seeds


def init_db():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        run_seeds(db)
