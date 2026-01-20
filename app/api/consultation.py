import os
from datetime import datetime
import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from app.db.session import get_db
from app.models.consultation import Consultation
from app.models.care_unit import CareUnit
from app.models.patient import Patient
from app.models.doctor import Doctor

from app.schemas.consultation import (
    ConsultationCreateSchema,
    ConsultationResponseSchema,
    ConsultationSummaryResponse,
)

from app.services.rule_based import generate_rule_based_summary

from app.services.llm_based import OllamaAsyncClient, OllamaError

router = APIRouter(prefix="/consultations", tags=["consultations"])

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ollama = OllamaAsyncClient(base_url=OLLAMA_URL, model="mistral")

async def ai_first_summary(
    consultation: Consultation, timeout_seconds: float = 1.0
) -> tuple[str, str]:

    prompt = f"""
        Resuma a consulta médica em 3 a 5 tópicos.

        Regras:
        - Não invente fatos
        - Não infira diagnósticos
        - Não prescreva tratamentos
        - Usar apenas dados fornecidos
        - Seja conciso.
        - Use apenas as informações fornecidas.

        Sintomas: {consultation.symptoms or "-"}
        Observações do paciente: {consultation.patient_notes or "-"}
        Observações médicas: {consultation.medical_notes or "-"}
        """.strip()

    try:
        text = await asyncio.wait_for(
            ollama.generate(
                prompt,
                stream=False,
                options={"temperature": 0.2},
                system="Você é um assistente médico. Retorne apenas o resumo.",
            ),
            timeout=timeout_seconds,
        )
        text = (text or "").strip()
        if text:
            return text, "llm_based"
    except (asyncio.TimeoutError, OllamaError):
        pass
    except Exception:
        pass

    return generate_rule_based_summary(consultation), "rule_based"


@router.post(
    "",
    response_model=ConsultationSummaryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_consultation(
    payload: ConsultationCreateSchema, db: Session = Depends(get_db)
):
    care_unit = db.get(CareUnit, payload.care_unit_id)
    if not care_unit:
        raise HTTPException(status_code=404, detail="Care unit not found")

    patient = db.get(Patient, payload.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    doctor = db.get(Doctor, payload.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    consultation = Consultation(
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
        care_unit_id=payload.care_unit_id,
        symptoms=payload.symptoms,
        patient_notes=payload.patient_notes,
        medical_notes=payload.medical_notes,
        appointment_datetime=payload.appointment_datetime,
    )

    db.add(consultation)
    db.commit()
    db.refresh(consultation)

    summary_text, strategy = await ai_first_summary(consultation)

    return ConsultationSummaryResponse(
        consultation_id=consultation.id,
        patient_name=patient.full_name,
        doctor_name=doctor.full_name,
        summary=summary_text,
        strategy=strategy,
        created_at=datetime.now(),
    )


@router.get("", response_model=list[ConsultationResponseSchema])
def list_consultations(db: Session = Depends(get_db)):
    stmt = select(Consultation).order_by(Consultation.id.desc())
    result = db.execute(stmt)
    return result.scalars().all()


@router.get("/{consultation_id}", response_model=ConsultationResponseSchema)
def get_consultation(consultation_id: int, db: Session = Depends(get_db)):
    consultation = db.get(Consultation, consultation_id)
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")
    return consultation


@router.get("/{consultation_id}/summary", response_model=ConsultationSummaryResponse)
async def get_consultation_summary(consultation_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(Consultation)
        .options(joinedload(Consultation.patient), joinedload(Consultation.doctor))
        .where(Consultation.id == consultation_id)
    )
    consultation = db.execute(stmt).scalars().first()

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    summary_text, strategy = await ai_first_summary(consultation)

    return ConsultationSummaryResponse(
        consultation_id=consultation.id,
        patient_name=consultation.patient.full_name,
        doctor_name=consultation.doctor.full_name,
        summary=summary_text,
        strategy=strategy,
        created_at=datetime.now(),
    )
