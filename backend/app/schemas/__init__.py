"""Pydantic schemas for request/response validation."""
from app.schemas.auth import Token, TokenRefresh, UserLogin, UserResponse, UserCreate
from app.schemas.feed import InboundFeedResponse, InboundFeedList, InboundFeedDetail
from app.schemas.product import ProductResponse, ProductList, ProductDetail, ProductCreate, ProductUpdate, BulkUpdateRequest
from app.schemas.outbound import OutboundJobResponse, OutboundJobList, OutboundJobDetail
from app.schemas.manufacturer import ManufacturerResponse, ManufacturerCreate, ManufacturerUpdate
from app.schemas.category import CategoryResponse, CategoryDetail
from app.schemas.attribute import AttributeResponse, AttributeCreate, AttributeUpdate
from app.schemas.log import SystemLogResponse
from app.schemas.common import PaginatedResponse

__all__ = [
    "Token",
    "TokenRefresh",
    "UserLogin",
    "UserResponse",
    "UserCreate",
    "InboundFeedResponse",
    "InboundFeedList",
    "InboundFeedDetail",
    "ProductResponse",
    "ProductList",
    "ProductDetail",
    "ProductCreate",
    "ProductUpdate",
    "BulkUpdateRequest",
    "OutboundJobResponse",
    "OutboundJobList",
    "OutboundJobDetail",
    "ManufacturerResponse",
    "ManufacturerCreate",
    "ManufacturerUpdate",
    "CategoryResponse",
    "CategoryDetail",
    "AttributeResponse",
    "AttributeCreate",
    "AttributeUpdate",
    "SystemLogResponse",
    "PaginatedResponse",
]
