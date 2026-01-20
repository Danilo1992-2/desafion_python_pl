from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False, index=True)
    document = Column(String(20), nullable=True, unique=True)
    birth_date = Column(String(10), nullable=True)

    consultations = relationship(
        "Consultation", back_populates="patient", cascade="all, delete-orphan"
    )
