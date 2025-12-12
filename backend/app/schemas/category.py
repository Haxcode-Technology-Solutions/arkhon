"""Category schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CategoryResponse(BaseModel):
    """Category response."""
    id: int
    name: str
    code: Optional[str] = None
    parent_id: Optional[int] = None
    description: Optional[str] = None
    level: int
    path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryDetail(CategoryResponse):
    """Detailed category response with product count."""
    product_count: int = 0
