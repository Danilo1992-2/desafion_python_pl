from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    care_unit_id = Column(Integer, ForeignKey("care_units.id"), nullable=False)

    symptoms = Column(String, nullable=False)
    patient_notes = Column(String(200), nullable=True)
    medical_notes = Column(String(200), nullable=True)
    appointment_datetime = Column(DateTime, nullable=False)

    patient = relationship("Patient", back_populates="consultations")
    doctor = relationship("Doctor", back_populates="consultations")
    care_unit = relationship("CareUnit", back_populates="consultations")
