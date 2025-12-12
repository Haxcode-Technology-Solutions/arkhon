"""Attribute schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AttributeResponse(BaseModel):
    """Attribute response."""
    id: int
    code: str
    label: str
    attribute_type: str
    input_type: str
    options: Optional[str] = None
    validation_rules: Optional[str] = None
    is_system: int
    is_searchable: int
    is_filterable: int
    sort_order: int
    group_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttributeCreate(BaseModel):
    """Attribute creation request."""
    code: str = Field(..., min_length=1, max_length=100)
    label: str = Field(..., min_length=1, max_length=255)
    attribute_type: str = Field(..., pattern="^(varchar|text|int|decimal|datetime|boolean)$")
    input_type: str = Field(..., pattern="^(text|textarea|select|multiselect|number|date|boolean)$")
    options: Optional[str] = None
    validation_rules: Optional[str] = None
    is_searchable: int = 1
    is_filterable: int = 1
    sort_order: int = 0
    group_name: Optional[str] = Field(None, max_length=100)


class AttributeUpdate(BaseModel):
    """Attribute update request."""
    label: Optional[str] = Field(None, min_length=1, max_length=255)
    options: Optional[str] = None
    validation_rules: Optional[str] = None
    is_searchable: Optional[int] = None
    is_filterable: Optional[int] = None
    sort_order: Optional[int] = None
    group_name: Optional[str] = Field(None, max_length=100)


class AttributeDetail(AttributeResponse):
    """Detailed attribute response with usage stats."""
    usage_count: int = 0
