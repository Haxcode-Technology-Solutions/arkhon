"""System logs API endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from datetime import datetime
import math

from app.core.database import get_db
from app.models.log import SystemLog, LogType, LogLevel
from app.schemas.log import SystemLogResponse
from app.schemas.common import PaginatedResponse
from app.api.dependencies import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("", response_model=PaginatedResponse[SystemLogResponse])
async def list_logs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    log_type: Optional[str] = None,
    log_level: Optional[str] = None,
    keyword: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """List system logs with filtering."""

    query = select(SystemLog)

    # Apply filters
    if log_type:
        try:
            log_type_enum = LogType(log_type)
            query = query.where(SystemLog.log_type == log_type_enum)
        except ValueError:
            pass

    if log_level:
        try:
            log_level_enum = LogLevel(log_level)
            query = query.where(SystemLog.log_level == log_level_enum)
        except ValueError:
            pass

    if keyword:
        query = query.where(
            or_(
                SystemLog.message.contains(keyword),
                SystemLog.context.contains(keyword)
            )
        )

    if start_date:
        query = query.where(SystemLog.created_at >= start_date)

    if end_date:
        query = query.where(SystemLog.created_at <= end_date)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.order_by(SystemLog.created_at.desc()).offset(offset).limit(page_size)

    result = await db.execute(query)
    logs = result.scalars().all()

    total_pages = math.ceil(total / page_size)

    return PaginatedResponse(
        items=logs,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/tail")
async def tail_logs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(100, ge=1, le=500),
    log_type: Optional[str] = None
):
    """Get latest logs (tail mode) for real-time monitoring."""

    query = select(SystemLog)

    if log_type:
        try:
            log_type_enum = LogType(log_type)
            query = query.where(SystemLog.log_type == log_type_enum)
        except ValueError:
            pass

    query = query.order_by(SystemLog.created_at.desc()).limit(limit)

    result = await db.execute(query)
    logs = result.scalars().all()

    return {"logs": [SystemLogResponse.model_validate(log) for log in logs]}
