"""System log model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SQLEnum, Index
import enum

from app.core.database import Base


class LogLevel(str, enum.Enum):
    """Log level."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogType(str, enum.Enum):
    """Log type/category."""
    IMPORT = "import"
    EXPORT = "export"
    CRON = "cron"
    AUTH = "auth"
    API = "api"
    SYSTEM = "system"


class SystemLog(Base):
    """System log model for tracking all system operations."""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    log_type = Column(SQLEnum(LogType), nullable=False, index=True)
    log_level = Column(SQLEnum(LogLevel), default=LogLevel.INFO, nullable=False, index=True)
    message = Column(Text, nullable=False)

    # Context data (JSON string)
    context = Column(Text)

    # User/system info
    user_id = Column(Integer, nullable=True)
    ip_address = Column(String(50))

    # Related entities
    entity_type = Column(String(50))  # e.g., 'feed', 'product', 'outbound_job'
    entity_id = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    __table_args__ = (
        Index('idx_log_search', 'log_type', 'log_level', 'created_at'),
    )
