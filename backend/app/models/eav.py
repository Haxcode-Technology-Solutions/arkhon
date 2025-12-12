"""EAV (Entity-Attribute-Value) models for flexible product attributes."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class AttributeType(str, enum.Enum):
    """Attribute data types."""
    VARCHAR = "varchar"
    TEXT = "text"
    INT = "int"
    DECIMAL = "decimal"
    DATETIME = "datetime"
    BOOLEAN = "boolean"


class AttributeInputType(str, enum.Enum):
    """Attribute input types for UI."""
    TEXT = "text"
    TEXTAREA = "textarea"
    SELECT = "select"
    MULTISELECT = "multiselect"
    NUMBER = "number"
    DATE = "date"
    BOOLEAN = "boolean"


class Attribute(Base):
    """Attribute definition model."""
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    label = Column(String(255), nullable=False)
    attribute_type = Column(SQLEnum(AttributeType), nullable=False)
    input_type = Column(SQLEnum(AttributeInputType), nullable=False)

    # Options for select/multiselect (stored as JSON string)
    options = Column(Text)

    # Validation rules (stored as JSON string)
    validation_rules = Column(Text)

    # Metadata
    is_system = Column(Integer, default=0)  # 1 for system, 0 for custom
    is_searchable = Column(Integer, default=1)
    is_filterable = Column(Integer, default=1)
    sort_order = Column(Integer, default=0)
    group_name = Column(String(100))  # For grouping in UI

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    values = relationship("AttributeValue", back_populates="attribute", cascade="all, delete-orphan")


class AttributeValue(Base):
    """Attribute value model - stores actual attribute values for products."""
    __tablename__ = "attribute_values"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    attribute_id = Column(Integer, ForeignKey("attributes.id", ondelete="CASCADE"), nullable=False)

    # Value storage (use appropriate column based on attribute type)
    value_varchar = Column(String(500))
    value_text = Column(Text)
    value_int = Column(Integer)
    value_decimal = Column(String(50))  # Stored as string to preserve precision
    value_datetime = Column(DateTime)
    value_boolean = Column(Integer)  # 0 or 1

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    product = relationship("Product", back_populates="attribute_values")
    attribute = relationship("Attribute", back_populates="values")

    __table_args__ = (
        Index('idx_product_attribute', 'product_id', 'attribute_id'),
    )
