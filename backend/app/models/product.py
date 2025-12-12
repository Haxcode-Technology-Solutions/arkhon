"""Product, category, and manufacturer models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Manufacturer(Base):
    """Manufacturer model."""
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    code = Column(String(100), unique=True, index=True)
    description = Column(Text)
    website = Column(String(500))
    is_system = Column(Integer, default=0)  # 1 for system-created, 0 for custom
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    products = relationship("Product", back_populates="manufacturer")


class Category(Base):
    """Category model."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    code = Column(String(100), unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    description = Column(Text)
    level = Column(Integer, default=0)
    path = Column(String(500))  # e.g., "Electronics/Computers/Laptops"
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    parent = relationship("Category", remote_side=[id], backref="children")
    product_categories = relationship("ProductCategory", back_populates="category")


class Product(Base):
    """Product model."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), nullable=False, index=True)
    entity_code = Column(String(50), nullable=False, index=True)  # Source entity
    name = Column(String(500), nullable=False)
    description = Column(Text)

    # Pricing
    price = Column(Numeric(10, 2), default=0.00)
    cost = Column(Numeric(10, 2))
    retail_price = Column(Numeric(10, 2))

    # Inventory
    qty = Column(Integer, default=0)
    min_qty = Column(Integer, default=0)

    # References
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"), nullable=True)

    # Images (stored as JSON string or comma-separated URLs)
    images = Column(Text)

    # Raw feed data (JSON)
    raw_data = Column(Text)

    # Metadata
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    manufacturer = relationship("Manufacturer", back_populates="products")
    categories = relationship("ProductCategory", back_populates="product", cascade="all, delete-orphan")
    attribute_values = relationship("AttributeValue", back_populates="product", cascade="all, delete-orphan")

    # Composite unique constraint
    __table_args__ = (
        UniqueConstraint('sku', 'entity_code', name='uix_sku_entity'),
        Index('idx_product_search', 'name', 'sku'),
    )


class ProductCategory(Base):
    """Many-to-many relationship between products and categories."""
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    is_primary = Column(Integer, default=0)  # 1 for primary category

    # Relationships
    product = relationship("Product", back_populates="categories")
    category = relationship("Category", back_populates="product_categories")

    __table_args__ = (
        UniqueConstraint('product_id', 'category_id', name='uix_product_category'),
    )
