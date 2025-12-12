"""Products API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import joinedload
from typing import Optional
from decimal import Decimal
import math
import json
import uuid
from datetime import datetime

from app.core.database import get_db
from app.models.product import Product, ProductCategory, Category, Manufacturer
from app.models.eav import AttributeValue, Attribute
from app.models.outbound import OutboundJob, OutboundStatus
from app.schemas.product import (
    ProductResponse, ProductList, ProductDetail, ProductUpdate,
    BulkUpdateRequest, BulkUpdateResponse, BulkUpdatePreview,
    CategoryRef, ManufacturerRef, AttributeValueRef
)
from app.schemas.common import PaginatedResponse
from app.api.dependencies import get_current_user, require_staff
from app.models.user import User


router = APIRouter()


@router.get("", response_model=PaginatedResponse[ProductList])
async def list_products(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sku: Optional[str] = None,
    name: Optional[str] = None,
    category_id: Optional[int] = None,
    manufacturer_id: Optional[int] = None,
    entity_code: Optional[str] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    min_stock: Optional[int] = None,
    max_stock: Optional[int] = None,
    search: Optional[str] = None
):
    """List products with server-side pagination and filtering."""

    # Build query
    query = select(Product).options(
        joinedload(Product.manufacturer),
        joinedload(Product.categories).joinedload(ProductCategory.category)
    )

    # Apply filters
    if sku:
        query = query.where(Product.sku.contains(sku))

    if name:
        query = query.where(Product.name.contains(name))

    if entity_code:
        query = query.where(Product.entity_code == entity_code)

    if manufacturer_id:
        query = query.where(Product.manufacturer_id == manufacturer_id)

    if category_id:
        query = query.join(ProductCategory).where(ProductCategory.category_id == category_id)

    if min_price is not None:
        query = query.where(Product.price >= min_price)

    if max_price is not None:
        query = query.where(Product.price <= max_price)

    if min_stock is not None:
        query = query.where(Product.qty >= min_stock)

    if max_stock is not None:
        query = query.where(Product.qty <= max_stock)

    if search:
        query = query.where(
            or_(
                Product.sku.contains(search),
                Product.name.contains(search),
                Product.description.contains(search)
            )
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    result = await db.execute(count_query)
    total = result.scalar_one()

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.order_by(Product.updated_at.desc()).offset(offset).limit(page_size)

    # Execute query
    result = await db.execute(query)
    products = result.unique().scalars().all()

    # Format response
    items = []
    for product in products:
        # Get primary category
        primary_category = None
        for pc in product.categories:
            if pc.is_primary:
                primary_category = CategoryRef(
                    id=pc.category.id,
                    name=pc.category.name,
                    code=pc.category.code
                )
                break

        # Get manufacturer
        manufacturer = None
        if product.manufacturer:
            manufacturer = ManufacturerRef(
                id=product.manufacturer.id,
                name=product.manufacturer.name,
                code=product.manufacturer.code
            )

        items.append(ProductList(
            id=product.id,
            sku=product.sku,
            name=product.name,
            price=product.price,
            qty=product.qty,
            manufacturer=manufacturer,
            primary_category=primary_category,
            entity_code=product.entity_code,
            updated_at=product.updated_at
        ))

    total_pages = math.ceil(total / page_size)

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{product_id}", response_model=ProductDetail)
async def get_product_detail(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed product information."""

    result = await db.execute(
        select(Product)
        .options(
            joinedload(Product.manufacturer),
            joinedload(Product.categories).joinedload(ProductCategory.category),
            joinedload(Product.attribute_values).joinedload(AttributeValue.attribute)
        )
        .where(Product.id == product_id)
    )
    product = result.unique().scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Format manufacturer
    manufacturer = None
    if product.manufacturer:
        manufacturer = ManufacturerRef(
            id=product.manufacturer.id,
            name=product.manufacturer.name,
            code=product.manufacturer.code
        )

    # Format categories
    categories = [
        CategoryRef(
            id=pc.category.id,
            name=pc.category.name,
            code=pc.category.code
        )
        for pc in product.categories
    ]

    # Format attributes
    attributes = []
    for av in product.attribute_values:
        # Get value based on attribute type
        value = None
        if av.attribute.attribute_type.value == "varchar":
            value = av.value_varchar
        elif av.attribute.attribute_type.value == "text":
            value = av.value_text
        elif av.attribute.attribute_type.value == "int":
            value = av.value_int
        elif av.attribute.attribute_type.value == "decimal":
            value = av.value_decimal
        elif av.attribute.attribute_type.value == "datetime":
            value = av.value_datetime.isoformat() if av.value_datetime else None
        elif av.attribute.attribute_type.value == "boolean":
            value = bool(av.value_boolean)

        attributes.append(AttributeValueRef(
            attribute_id=av.attribute.id,
            attribute_code=av.attribute.code,
            attribute_label=av.attribute.label,
            value=value
        ))

    return ProductDetail(
        id=product.id,
        sku=product.sku,
        entity_code=product.entity_code,
        name=product.name,
        description=product.description,
        price=product.price,
        cost=product.cost,
        retail_price=product.retail_price,
        qty=product.qty,
        min_qty=product.min_qty,
        manufacturer_id=product.manufacturer_id,
        images=product.images,
        raw_data=product.raw_data,
        is_active=product.is_active,
        created_at=product.created_at,
        updated_at=product.updated_at,
        manufacturer=manufacturer,
        categories=categories,
        attributes=attributes
    )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """Update product."""

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Update fields
    update_data = product_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field not in ["category_ids", "attributes"]:
            setattr(product, field, value)

    # Update categories if provided
    if product_update.category_ids is not None:
        # Remove existing categories
        await db.execute(
            select(ProductCategory).where(ProductCategory.product_id == product_id)
        )
        # Add new categories
        for cat_id in product_update.category_ids:
            pc = ProductCategory(product_id=product_id, category_id=cat_id)
            db.add(pc)

    await db.commit()
    await db.refresh(product)

    return product


@router.post("/bulk-update", response_model=BulkUpdateResponse)
async def bulk_update_products(
    bulk_update: BulkUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff)
):
    """Bulk update product prices or quantities."""

    # Get products
    result = await db.execute(
        select(Product).where(Product.id.in_(bulk_update.product_ids))
    )
    products = result.scalars().all()

    if len(products) != len(bulk_update.product_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Some products not found"
        )

    # Calculate preview
    preview = []
    bulk_data = {
        "target_field": bulk_update.target_field,
        "mode": bulk_update.mode,
        "value": str(bulk_update.value),
        "reason": bulk_update.reason,
        "changes": []
    }

    for product in products:
        old_value = getattr(product, bulk_update.target_field)

        # Calculate new value
        if bulk_update.mode == "percent":
            new_value = old_value * (1 + (bulk_update.value / 100))
        else:  # fixed
            new_value = old_value + bulk_update.value

        # Ensure non-negative
        new_value = max(Decimal(0), new_value)

        preview.append(BulkUpdatePreview(
            product_id=product.id,
            sku=product.sku,
            name=product.name,
            old_value=old_value,
            new_value=new_value
        ))

        bulk_data["changes"].append({
            "product_id": product.id,
            "sku": product.sku,
            "old_value": str(old_value),
            "new_value": str(new_value)
        })

    # Create outbound job
    sync_id = f"bulk_update_{uuid.uuid4().hex[:8]}"
    skus = ",".join([p.sku for p in products])

    outbound_job = OutboundJob(
        sync_id=sync_id,
        job_type="bulk_update",
        status=OutboundStatus.PENDING,
        skus=skus,
        bulk_data=json.dumps(bulk_data),
        total_count=len(products),
        success_count=0,
        error_count=0
    )

    db.add(outbound_job)
    await db.commit()
    await db.refresh(outbound_job)

    # TODO: Trigger Celery task to process bulk update
    # from app.workers.tasks import process_bulk_update
    # process_bulk_update.delay(outbound_job.id)

    return BulkUpdateResponse(
        job_id=outbound_job.id,
        sync_id=sync_id,
        total_products=len(products),
        preview=preview,
        message="Bulk update job created successfully"
    )
