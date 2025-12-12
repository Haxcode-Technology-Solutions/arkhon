"""Inbound feeds API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from datetime import datetime
import math

from app.core.database import get_db
from app.models.feed import InboundFeed, FeedStatus
from app.schemas.feed import InboundFeedResponse, InboundFeedDetail, InboundFeedList
from app.schemas.common import PaginatedResponse
from app.api.dependencies import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("", response_model=PaginatedResponse[InboundFeedList])
async def list_feeds(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    entity_code: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """List inbound feeds with server-side pagination and filtering."""

    # Build query
    query = select(InboundFeed)

    # Apply filters
    if entity_code:
        query = query.where(InboundFeed.entity_code == entity_code)

    if status:
        try:
            status_enum = FeedStatus(status)
            query = query.where(InboundFeed.status == status_enum)
        except ValueError:
            pass

    if search:
        query = query.where(
            or_(
                InboundFeed.file_name.contains(search),
                InboundFeed.entity_code.contains(search)
            )
        )

    if start_date:
        query = query.where(InboundFeed.created_at >= start_date)

    if end_date:
        query = query.where(InboundFeed.created_at <= end_date)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.order_by(InboundFeed.created_at.desc()).offset(offset).limit(page_size)

    # Execute query
    result = await db.execute(query)
    feeds = result.scalars().all()

    total_pages = math.ceil(total / page_size)

    return PaginatedResponse(
        items=feeds,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{feed_id}", response_model=InboundFeedDetail)
async def get_feed_detail(
    feed_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed feed information."""

    result = await db.execute(select(InboundFeed).where(InboundFeed.id == feed_id))
    feed = result.scalar_one_or_none()

    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found"
        )

    return feed


@router.get("/{feed_id}/logs")
async def get_feed_logs(
    feed_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get feed processing logs."""

    result = await db.execute(select(InboundFeed).where(InboundFeed.id == feed_id))
    feed = result.scalar_one_or_none()

    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found"
        )

    return {
        "feed_id": feed.id,
        "processing_logs": feed.processing_logs,
        "error_message": feed.error_message
    }


@router.post("/{feed_id}/retry")
async def retry_feed_import(
    feed_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retry failed feed import."""

    result = await db.execute(select(InboundFeed).where(InboundFeed.id == feed_id))
    feed = result.scalar_one_or_none()

    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feed not found"
        )

    if feed.status not in [FeedStatus.FAILED, FeedStatus.PARTIAL]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only failed or partial feeds can be retried"
        )

    # Reset feed status
    feed.status = FeedStatus.PENDING
    feed.error_message = None
    await db.commit()

    # TODO: Trigger import task via Celery
    # from app.workers.tasks import import_feed_task
    # import_feed_task.delay(feed.id)

    return {
        "message": "Feed import retry initiated",
        "feed_id": feed.id
    }
