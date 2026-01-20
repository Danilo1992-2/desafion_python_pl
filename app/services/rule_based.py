from app.models.consultation import Consultation


def generate_rule_based_summary(consultation: Consultation) -> str:
    parts: list[str] = []

    parts.append(
        f"Consulta agendada em {consultation.appointment_datetime:%Y-%m-%d %H:%M}."
    )
    parts.append(f"Sintomas relatados: {consultation.symptoms}.")

    if consultation.patient_notes:
        parts.append(f"Relato do paciente: {consultation.patient_notes}.")
    if consultation.medical_notes:
        parts.append(f"Anotações médicas: {consultation.medical_notes}.")

    return " ".join(parts)
