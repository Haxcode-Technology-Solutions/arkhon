"""Inbound feed models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum
import enum

from app.core.database import Base


class FeedStatus(str, enum.Enum):
    """Feed processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class InboundFeed(Base):
    """Inbound feed model for tracking imported files."""
    __tablename__ = "inbound_feeds"

    id = Column(Integer, primary_key=True, index=True)
    entity_code = Column(String(50), index=True, nullable=False)  # e.g., 'bigbuy'
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)  # in bytes
    status = Column(SQLEnum(FeedStatus), default=FeedStatus.PENDING, nullable=False, index=True)

    # Processing stats
    total_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    pending_count = Column(Integer, default=0)

    # Metadata
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    processing_logs = Column(Text)  # JSON string of processing logs

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
