"""Dashboard API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any, List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.product import Product
from app.models.feed import InboundFeed, FeedStatus
from app.models.outbound import OutboundJob, OutboundStatus
from app.api.dependencies import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get dashboard statistics."""

    # Total products
    result = await db.execute(select(func.count(Product.id)))
    total_products = result.scalar_one()

    # Total outbound jobs
    result = await db.execute(select(func.count(OutboundJob.id)))
    total_outbound_jobs = result.scalar_one()

    # Pending inbound feeds
    result = await db.execute(
        select(func.count(InboundFeed.id)).where(
            InboundFeed.status.in_([FeedStatus.PENDING, FeedStatus.PROCESSING])
        )
    )
    pending_feeds = result.scalar_one()

    # Failed inbound feeds
    result = await db.execute(
        select(func.count(InboundFeed.id)).where(InboundFeed.status == FeedStatus.FAILED)
    )
    failed_feeds = result.scalar_one()

    # Queue status - pending outbound jobs
    result = await db.execute(
        select(func.count(OutboundJob.id)).where(
            OutboundJob.status.in_([OutboundStatus.PENDING, OutboundStatus.PROCESSING])
        )
    )
    queue_pending = result.scalar_one()

    # Recent activity summary
    seven_days_ago = datetime.utcnow() - timedelta(days=7)

    # Products added in last 7 days
    result = await db.execute(
        select(func.count(Product.id)).where(Product.created_at >= seven_days_ago)
    )
    products_last_7_days = result.scalar_one()

    # Feeds processed in last 7 days
    result = await db.execute(
        select(func.count(InboundFeed.id)).where(InboundFeed.created_at >= seven_days_ago)
    )
    feeds_last_7_days = result.scalar_one()

    return {
        "total_products": total_products,
        "total_outbound_jobs": total_outbound_jobs,
        "pending_inbound_feeds": pending_feeds,
        "failed_inbound_feeds": failed_feeds,
        "queue_status": {
            "pending": queue_pending
        },
        "recent_activity": {
            "products_last_7_days": products_last_7_days,
            "feeds_last_7_days": feeds_last_7_days
        }
    }


@router.get("/timeline")
async def get_timeline(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 20
) -> Dict[str, List[Dict[str, Any]]]:
    """Get recent timeline of operations."""

    # Get recent feeds
    result = await db.execute(
        select(InboundFeed)
        .order_by(InboundFeed.created_at.desc())
        .limit(limit)
    )
    recent_feeds = result.scalars().all()

    # Get recent outbound jobs
    result = await db.execute(
        select(OutboundJob)
        .order_by(OutboundJob.created_at.desc())
        .limit(limit)
    )
    recent_outbound = result.scalars().all()

    # Combine and format timeline
    timeline = []

    for feed in recent_feeds:
        timeline.append({
            "type": "inbound_feed",
            "id": feed.id,
            "entity_code": feed.entity_code,
            "file_name": feed.file_name,
            "status": feed.status.value,
            "timestamp": feed.created_at.isoformat(),
            "details": {
                "total_count": feed.total_count,
                "success_count": feed.success_count,
                "error_count": feed.error_count
            }
        })

    for job in recent_outbound:
        timeline.append({
            "type": "outbound_job",
            "id": job.id,
            "sync_id": job.sync_id,
            "status": job.status.value,
            "timestamp": job.created_at.isoformat(),
            "details": {
                "total_count": job.total_count,
                "success_count": job.success_count,
                "error_count": job.error_count
            }
        })

    # Sort by timestamp
    timeline.sort(key=lambda x: x["timestamp"], reverse=True)

    return {"timeline": timeline[:limit]}
