"""Manufacturers API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import math

from app.core.database import get_db
from app.models.product import Manufacturer
from app.schemas.manufacturer import ManufacturerResponse, ManufacturerCreate, ManufacturerUpdate
from app.schemas.common import PaginatedResponse
from app.api.dependencies import get_current_user, require_staff
from app.models.user import User


router = APIRouter()


@router.get("", response_model=PaginatedResponse[ManufacturerResponse])
async def list_manufacturers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200)
):
    """List all manufacturers."""

    query = select(Manufacturer)

    # Get total count
    count_query = select(func.count(Manufacturer.id))
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.order_by(Manufacturer.name).offset(offset).limit(page_size)

    result = await db.execute(query)
    manufacturers = result.scalars().all()

    total_pages = math.ceil(total / page_size)

    return PaginatedResponse(
        items=manufacturers,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post("", response_model=ManufacturerResponse)
async def create_manufacturer(
    manufacturer_data: ManufacturerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """Create a new manufacturer."""

    # Check if name already exists
    result = await db.execute(
        select(Manufacturer).where(Manufacturer.name == manufacturer_data.name)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Manufacturer with this name already exists"
        )

    manufacturer = Manufacturer(**manufacturer_data.model_dump())
    db.add(manufacturer)
    await db.commit()
    await db.refresh(manufacturer)

    return manufacturer


@router.get("/{manufacturer_id}", response_model=ManufacturerResponse)
async def get_manufacturer(
    manufacturer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get manufacturer details."""

    result = await db.execute(
        select(Manufacturer).where(Manufacturer.id == manufacturer_id)
    )
    manufacturer = result.scalar_one_or_none()

    if not manufacturer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manufacturer not found"
        )

    return manufacturer


@router.put("/{manufacturer_id}", response_model=ManufacturerResponse)
async def update_manufacturer(
    manufacturer_id: int,
    manufacturer_update: ManufacturerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """Update manufacturer."""

    result = await db.execute(
        select(Manufacturer).where(Manufacturer.id == manufacturer_id)
    )
    manufacturer = result.scalar_one_or_none()

    if not manufacturer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manufacturer not found"
        )

    if manufacturer.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update system manufacturer"
        )

    update_data = manufacturer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(manufacturer, field, value)

    await db.commit()
    await db.refresh(manufacturer)

    return manufacturer


@router.delete("/{manufacturer_id}")
async def delete_manufacturer(
    manufacturer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """Delete manufacturer."""

    result = await db.execute(
        select(Manufacturer).where(Manufacturer.id == manufacturer_id)
    )
    manufacturer = result.scalar_one_or_none()

    if not manufacturer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manufacturer not found"
        )

    if manufacturer.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete system manufacturer"
        )

    await db.delete(manufacturer)
    await db.commit()

    return {"message": "Manufacturer deleted successfully"}
