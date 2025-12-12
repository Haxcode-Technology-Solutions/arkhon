"""Cron and task management API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from datetime import datetime

from app.api.dependencies import get_current_user, require_staff
from app.models.user import User


router = APIRouter()


@router.get("/status")
async def get_cron_status(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get cron/scheduled tasks status."""

    # In production, this would check actual cron/celery beat status
    # For now, return mock data

    return {
        "tasks": [
            {
                "name": "fetch_feeds",
                "description": "Fetch product feeds from FTP",
                "schedule": "0 2 * * *",  # Daily at 2 AM
                "last_run": datetime.utcnow().isoformat(),
                "next_run": datetime.utcnow().isoformat(),
                "status": "active",
                "last_status": "success"
            },
            {
                "name": "import_feeds",
                "description": "Import downloaded product feeds",
                "schedule": "0 3 * * *",  # Daily at 3 AM
                "last_run": datetime.utcnow().isoformat(),
                "next_run": datetime.utcnow().isoformat(),
                "status": "active",
                "last_status": "success"
            },
            {
                "name": "sync_outbound",
                "description": "Sync products to outbound systems",
                "schedule": "*/30 * * * *",  # Every 30 minutes
                "last_run": datetime.utcnow().isoformat(),
                "next_run": datetime.utcnow().isoformat(),
                "status": "active",
                "last_status": "success"
            }
        ],
        "worker_status": {
            "active": True,
            "workers": 3,
            "pending_tasks": 5
        }
    }


@router.post("/run/{task_name}")
async def trigger_task(
    task_name: str,
    current_user: User = Depends(require_staff)
) -> Dict[str, Any]:
    """Manually trigger a cron task."""

    valid_tasks = ["fetch_feeds", "import_feeds", "sync_outbound"]

    if task_name not in valid_tasks:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid task name. Valid tasks: {', '.join(valid_tasks)}"
        )

    # In production, this would trigger actual Celery tasks
    # TODO: Implement actual task triggering
    # if task_name == "fetch_feeds":
    #     from app.workers.tasks import fetch_feeds_task
    #     task = fetch_feeds_task.delay()
    # elif task_name == "import_feeds":
    #     from app.workers.tasks import import_latest_feed_task
    #     task = import_latest_feed_task.delay()
    # elif task_name == "sync_outbound":
    #     from app.workers.tasks import sync_outbound_products_task
    #     task = sync_outbound_products_task.delay()

    return {
        "message": f"Task '{task_name}' triggered successfully",
        "task_name": task_name,
        "triggered_by": current_user.username,
        "triggered_at": datetime.utcnow().isoformat()
    }
