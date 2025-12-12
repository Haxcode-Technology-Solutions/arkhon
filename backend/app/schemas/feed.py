"""Inbound feed schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InboundFeedResponse(BaseModel):
    """Inbound feed response."""
    id: int
    entity_code: str
    file_name: str
    file_path: str
    file_size: Optional[int] = None
    status: str
    total_count: int
    success_count: int
    error_count: int
    pending_count: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InboundFeedDetail(InboundFeedResponse):
    """Detailed inbound feed response with logs."""
    processing_logs: Optional[str] = None


class InboundFeedList(BaseModel):
    """Inbound feed list item."""
    id: int
    entity_code: str
    file_name: str
    status: str
    total_count: int
    success_count: int
    error_count: int
    pending_count: int
    updated_at: datetime

    class Config:
        from_attributes = True
