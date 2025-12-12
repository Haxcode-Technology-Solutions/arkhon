"""Outbound job models for product synchronization."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum
import enum

from app.core.database import Base


class OutboundStatus(str, enum.Enum):
    """Outbound job status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


class OutboundJob(Base):
    """Outbound job model for tracking product sync operations."""
    __tablename__ = "outbound_jobs"

    id = Column(Integer, primary_key=True, index=True)
    sync_id = Column(String(100), unique=True, index=True)  # Unique identifier for the sync
    job_type = Column(String(50), default="product_sync")  # Type of sync operation
    status = Column(SQLEnum(OutboundStatus), default=OutboundStatus.PENDING, nullable=False, index=True)

    # SKUs being synced (comma-separated)
    skus = Column(Text)

    # Bulk operation data (JSON string with operation details)
    bulk_data = Column(Text)

    # Processing info
    total_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)

    # Retry info
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)

    # Messages and logs
    message = Column(Text)
    processing_logs = Column(Text)  # JSON string of logs

    # Timestamps
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    next_retry_at = Column(DateTime)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
