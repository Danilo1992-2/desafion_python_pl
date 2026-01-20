from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.init_db import init_db
from app.api.consultation import router as consultation_router
from app.api.patient import router as patient_router
from app.api.doctor import router as doctor_router
from app.api.care_unit import router as care_unit_router
from app.api.symptom import router as symptom_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Healthtech API", lifespan=lifespan)

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(care_unit_router)
app.include_router(consultation_router)
app.include_router(symptom_router)
