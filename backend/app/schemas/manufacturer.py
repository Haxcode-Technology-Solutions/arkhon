"""Manufacturer schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ManufacturerResponse(BaseModel):
    """Manufacturer response."""
    id: int
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    is_system: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ManufacturerCreate(BaseModel):
    """Manufacturer creation request."""
    name: str = Field(..., min_length=1, max_length=255)
    code: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    website: Optional[str] = Field(None, max_length=500)


class ManufacturerUpdate(BaseModel):
    """Manufacturer update request."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    website: Optional[str] = Field(None, max_length=500)
