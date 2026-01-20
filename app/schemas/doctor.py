from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class DoctorCreateSchema(BaseModel):
    full_name: str = Field(..., description="Doctor full name")
    crm: Optional[str] = Field(None, description="Medical license number (CRM)")
    specialty: Optional[str] = Field(None, description="Medical specialty")


class DoctorResponseSchema(BaseModel):
    id: int
    full_name: str
    crm: Optional[str] = None
    specialty: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
