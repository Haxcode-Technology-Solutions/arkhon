"""Attributes API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import math

from app.core.database import get_db
from app.models.eav import Attribute, AttributeValue
from app.schemas.attribute import AttributeResponse, AttributeCreate, AttributeUpdate, AttributeDetail
from app.schemas.common import PaginatedResponse
from app.api.dependencies import get_current_user, require_staff
from app.models.user import User


router = APIRouter()


@router.get("", response_model=PaginatedResponse[AttributeResponse])
async def list_attributes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200)
):
    """List all attributes."""

    query = select(Attribute)

    # Get total count
    count_query = select(func.count(Attribute.id))
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.order_by(Attribute.sort_order, Attribute.label).offset(offset).limit(page_size)

    result = await db.execute(query)
    attributes = result.scalars().all()

    total_pages = math.ceil(total / page_size)

    return PaginatedResponse(
        items=attributes,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.post("", response_model=AttributeResponse)
async def create_attribute(
    attribute_data: AttributeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """Create a new attribute."""

    # Check if code already exists
    result = await db.execute(
        select(Attribute).where(Attribute.code == attribute_data.code)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attribute with this code already exists"
        )

    attribute = Attribute(**attribute_data.model_dump())
    db.add(attribute)
    await db.commit()
    await db.refresh(attribute)

    return attribute


@router.get("/{attribute_id}", response_model=AttributeDetail)
async def get_attribute(
    attribute_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get attribute details with usage count."""

    result = await db.execute(
        select(Attribute).where(Attribute.id == attribute_id)
    )
    attribute = result.scalar_one_or_none()

    if not attribute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attribute not found"
        )

    # Get usage count
    count_result = await db.execute(
        select(func.count(AttributeValue.id)).where(
            AttributeValue.attribute_id == attribute_id
        )
    )
    usage_count = count_result.scalar_one()

    return AttributeDetail(
        id=attribute.id,
        code=attribute.code,
        label=attribute.label,
        attribute_type=attribute.attribute_type.value,
        input_type=attribute.input_type.value,
        options=attribute.options,
        validation_rules=attribute.validation_rules,
        is_system=attribute.is_system,
        is_searchable=attribute.is_searchable,
        is_filterable=attribute.is_filterable,
        sort_order=attribute.sort_order,
        group_name=attribute.group_name,
        created_at=attribute.created_at,
        updated_at=attribute.updated_at,
        usage_count=usage_count
    )


@router.put("/{attribute_id}", response_model=AttributeResponse)
async def update_attribute(
    attribute_id: int,
    attribute_update: AttributeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """Update attribute."""

    result = await db.execute(
        select(Attribute).where(Attribute.id == attribute_id)
    )
    attribute = result.scalar_one_or_none()

    if not attribute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attribute not found"
        )

    if attribute.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update system attribute"
        )

    update_data = attribute_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(attribute, field, value)

    await db.commit()
    await db.refresh(attribute)

    return attribute


@router.delete("/{attribute_id}")
async def delete_attribute(
    attribute_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """Delete attribute."""

    result = await db.execute(
        select(Attribute).where(Attribute.id == attribute_id)
    )
    attribute = result.scalar_one_or_none()

    if not attribute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attribute not found"
        )

    if attribute.is_system:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete system attribute"
        )

    await db.delete(attribute)
    await db.commit()

    return {"message": "Attribute deleted successfully"}
