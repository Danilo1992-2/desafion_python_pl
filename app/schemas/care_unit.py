from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CareUnitCreateSchema(BaseModel):
    name: str = Field(..., description="Hospital / care unit name")
    cnes: Optional[str] = Field(None, description="CNES code (optional)")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State (UF)")


class CareUnitResponseSchema(BaseModel):
    id: int
    name: str
    cnes: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
