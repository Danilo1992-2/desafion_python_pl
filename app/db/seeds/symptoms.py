from pathlib import Path
import csv
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.symptom import Symptom

SEEDS_DIR = Path(__file__).resolve().parent
CSV_PATH = SEEDS_DIR / "symptoms.csv"


def seed_symptoms(db: Session):
    count = db.scalar(select(func.count()).select_from(Symptom))
    if count and count > 0:
        return

    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            name = (r.get("name") or "").strip()
            if name:
                rows.append(Symptom(name=name, category=r.get("category")))

    db.add_all(rows)
    db.commit()
