"""Outbound jobs API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
import math

from app.core.database import get_db
from app.models.outbound import OutboundJob, OutboundStatus
from app.schemas.outbound import OutboundJobResponse, OutboundJobList, OutboundJobDetail
from app.schemas.common import PaginatedResponse
from app.api.dependencies import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("", response_model=PaginatedResponse[OutboundJobList])
async def list_outbound_jobs(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None
):
    """List outbound jobs with pagination."""

    query = select(OutboundJob)

    if status:
        try:
            status_enum = OutboundStatus(status)
            query = query.where(OutboundJob.status == status_enum)
        except ValueError:
            pass

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.order_by(OutboundJob.created_at.desc()).offset(offset).limit(page_size)

    result = await db.execute(query)
    jobs = result.scalars().all()

    total_pages = math.ceil(total / page_size)

    return PaginatedResponse(
        items=jobs,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{job_id}", response_model=OutboundJobDetail)
async def get_outbound_job_detail(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed outbound job information."""

    result = await db.execute(select(OutboundJob).where(OutboundJob.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Outbound job not found"
        )

    return job


@router.post("/{job_id}/retry")
async def retry_outbound_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retry failed outbound job."""

    result = await db.execute(select(OutboundJob).where(OutboundJob.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Outbound job not found"
        )

    if job.status not in [OutboundStatus.FAILED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only failed jobs can be retried"
        )

    if job.retry_count >= job.max_retries:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum retry attempts reached"
        )

    # Reset job status
    job.status = OutboundStatus.PENDING
    job.retry_count += 1
    await db.commit()

    # TODO: Trigger Celery task
    # from app.workers.tasks import process_outbound_job
    # process_outbound_job.delay(job.id)

    return {
        "message": "Outbound job retry initiated",
        "job_id": job.id
    }
