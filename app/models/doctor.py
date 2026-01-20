from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False, index=True)
    crm = Column(String(20), nullable=True, unique=True)
    specialty = Column(String(100), nullable=True)

    consultations = relationship(
        "Consultation", back_populates="doctor", cascade="all, delete-orphan"
    )
