"""System log schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SystemLogResponse(BaseModel):
    """System log response."""
    id: int
    log_type: str
    log_level: str
    message: str
    context: Optional[str] = None
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SystemLogCreate(BaseModel):
    """System log creation request."""
    log_type: str
    log_level: str
    message: str
    context: Optional[str] = None
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None
