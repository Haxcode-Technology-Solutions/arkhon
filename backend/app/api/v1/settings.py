"""Settings API endpoints."""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from pydantic import BaseModel

from app.api.dependencies import get_current_user, require_admin
from app.models.user import User


router = APIRouter()


class SettingsResponse(BaseModel):
    """Settings response model."""
    entity_settings: Dict[str, Any]
    ftp_settings: Dict[str, Any]
    storage_settings: Dict[str, Any]
    sync_settings: Dict[str, Any]


class SettingsUpdate(BaseModel):
    """Settings update model."""
    entity_settings: Dict[str, Any] = {}
    ftp_settings: Dict[str, Any] = {}
    storage_settings: Dict[str, Any] = {}
    sync_settings: Dict[str, Any] = {}


@router.get("", response_model=SettingsResponse)
async def get_settings(
    current_user: User = Depends(require_admin)
):
    """Get application settings (admin only)."""

    # In production, these would be stored in database or config management system
    # For now, return static configuration

    return SettingsResponse(
        entity_settings={
            "bigbuy": {
                "enabled": True,
                "entity_code": "bigbuy",
                "name": "BigBuy"
            }
        },
        ftp_settings={
            "bigbuy": {
                "host": "ftp.bigbuy.eu",
                "port": 21,
                "username": "****",
                "path": "/products"
            }
        },
        storage_settings={
            "type": "local",
            "path": "./storage"
        },
        sync_settings={
            "retry_attempts": 3,
            "retry_delay": 5,
            "batch_size": 1000
        }
    )


@router.post("", response_model=SettingsResponse)
async def update_settings(
    settings_update: SettingsUpdate,
    current_user: User = Depends(require_admin)
):
    """Update application settings (admin only)."""

    # In production, save these to database or config management system
    # For now, just return the updated settings

    # This is a placeholder implementation
    # In real system, you would:
    # 1. Validate settings
    # 2. Save to database/config store
    # 3. Potentially restart services if needed

    return SettingsResponse(
        entity_settings=settings_update.entity_settings,
        ftp_settings=settings_update.ftp_settings,
        storage_settings=settings_update.storage_settings,
        sync_settings=settings_update.sync_settings
    )
