from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SymptomCreateSchema(BaseModel):
    name: str = Field(..., description="Symptom name (e.g., Fever, Headache)")
    description: Optional[str] = Field(None, description="Optional description")


class SymptomResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
