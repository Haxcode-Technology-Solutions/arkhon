"""Categories API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
import math

from app.core.database import get_db
from app.models.product import Category, ProductCategory, Product
from app.schemas.category import CategoryResponse, CategoryDetail
from app.schemas.product import ProductList
from app.schemas.common import PaginatedResponse
from app.api.dependencies import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("", response_model=PaginatedResponse[CategoryResponse])
async def list_categories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200)
):
    """List all categories."""

    query = select(Category)

    # Get total count
    count_query = select(func.count(Category.id))
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.order_by(Category.path).offset(offset).limit(page_size)

    result = await db.execute(query)
    categories = result.scalars().all()

    total_pages = math.ceil(total / page_size)

    return PaginatedResponse(
        items=categories,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{category_id}", response_model=CategoryDetail)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get category details with product count."""

    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Get product count
    count_result = await db.execute(
        select(func.count(ProductCategory.id)).where(
            ProductCategory.category_id == category_id
        )
    )
    product_count = count_result.scalar_one()

    return CategoryDetail(
        id=category.id,
        name=category.name,
        code=category.code,
        parent_id=category.parent_id,
        description=category.description,
        level=category.level,
        path=category.path,
        created_at=category.created_at,
        updated_at=category.updated_at,
        product_count=product_count
    )


@router.get("/{category_id}/products", response_model=PaginatedResponse[ProductList])
async def get_category_products(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """Get all products in a category."""

    # Verify category exists
    result = await db.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # Get products
    query = (
        select(Product)
        .join(ProductCategory)
        .where(ProductCategory.category_id == category_id)
        .options(joinedload(Product.manufacturer))
    )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    products = result.unique().scalars().all()

    # Format response (simplified for category view)
    items = [
        ProductList(
            id=p.id,
            sku=p.sku,
            name=p.name,
            price=p.price,
            qty=p.qty,
            manufacturer=None,
            primary_category=None,
            entity_code=p.entity_code,
            updated_at=p.updated_at
        )
        for p in products
    ]

    total_pages = math.ceil(total / page_size)

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )
