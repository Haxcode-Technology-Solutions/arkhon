"""Product schemas."""
from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal
from pydantic import BaseModel, Field


class CategoryRef(BaseModel):
    """Category reference."""
    id: int
    name: str
    code: Optional[str] = None


class ManufacturerRef(BaseModel):
    """Manufacturer reference."""
    id: int
    name: str
    code: Optional[str] = None


class AttributeValueRef(BaseModel):
    """Attribute value reference."""
    attribute_id: int
    attribute_code: str
    attribute_label: str
    value: Any


class ProductResponse(BaseModel):
    """Basic product response."""
    id: int
    sku: str
    entity_code: str
    name: str
    description: Optional[str] = None
    price: Decimal
    qty: int
    manufacturer_id: Optional[int] = None
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductList(BaseModel):
    """Product list item."""
    id: int
    sku: str
    name: str
    price: Decimal
    qty: int
    manufacturer: Optional[ManufacturerRef] = None
    primary_category: Optional[CategoryRef] = None
    entity_code: str
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductDetail(ProductResponse):
    """Detailed product response."""
    cost: Optional[Decimal] = None
    retail_price: Optional[Decimal] = None
    min_qty: int = 0
    images: Optional[str] = None
    raw_data: Optional[str] = None
    manufacturer: Optional[ManufacturerRef] = None
    categories: List[CategoryRef] = []
    attributes: List[AttributeValueRef] = []


class ProductCreate(BaseModel):
    """Product creation request."""
    sku: str = Field(..., min_length=1, max_length=100)
    entity_code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    price: Decimal = Field(default=0, ge=0)
    cost: Optional[Decimal] = Field(default=None, ge=0)
    retail_price: Optional[Decimal] = Field(default=None, ge=0)
    qty: int = Field(default=0, ge=0)
    min_qty: int = Field(default=0, ge=0)
    manufacturer_id: Optional[int] = None
    category_ids: List[int] = []
    images: Optional[str] = None
    raw_data: Optional[str] = None
    attributes: Dict[str, Any] = {}


class ProductUpdate(BaseModel):
    """Product update request."""
    name: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    cost: Optional[Decimal] = Field(None, ge=0)
    retail_price: Optional[Decimal] = Field(None, ge=0)
    qty: Optional[int] = Field(None, ge=0)
    min_qty: Optional[int] = Field(None, ge=0)
    manufacturer_id: Optional[int] = None
    category_ids: Optional[List[int]] = None
    images: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    is_active: Optional[int] = None


class BulkUpdateRequest(BaseModel):
    """Bulk update request."""
    product_ids: List[int] = Field(..., min_items=1)
    target_field: str = Field(..., pattern="^(price|qty)$")  # Only price or qty
    mode: str = Field(..., pattern="^(percent|fixed)$")  # percent or fixed adjustment
    value: Decimal = Field(...)
    reason: Optional[str] = None


class BulkUpdatePreview(BaseModel):
    """Bulk update preview item."""
    product_id: int
    sku: str
    name: str
    old_value: Decimal
    new_value: Decimal


class BulkUpdateResponse(BaseModel):
    """Bulk update response."""
    job_id: int
    sync_id: str
    total_products: int
    preview: List[BulkUpdatePreview]
    message: str
