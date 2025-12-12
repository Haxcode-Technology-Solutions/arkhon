"""Outbound job schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OutboundJobResponse(BaseModel):
    """Outbound job response."""
    id: int
    sync_id: str
    job_type: str
    status: str
    total_count: int
    success_count: int
    error_count: int
    retry_count: int
    max_retries: int
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OutboundJobList(BaseModel):
    """Outbound job list item."""
    id: int
    sync_id: str
    status: str
    message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OutboundJobDetail(OutboundJobResponse):
    """Detailed outbound job response."""
    skus: Optional[str] = None
    bulk_data: Optional[str] = None
    processing_logs: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    next_retry_at: Optional[datetime] = None
