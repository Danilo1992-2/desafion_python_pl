from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class PatientCreateSchema(BaseModel):
    full_name: str = Field(..., description="Patient full name")
    document: Optional[str] = Field(None, description="Patient document (CPF/ID)")
    birth_date: Optional[str] = Field(None, description="Birth date (YYYY-MM-DD)")


class PatientResponseSchema(BaseModel):
    id: int
    full_name: str

    model_config = ConfigDict(from_attributes=True)
