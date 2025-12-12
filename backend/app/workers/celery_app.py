"""Celery application configuration."""
from celery import Celery
from app.core.config import settings


# Create Celery app
celery_app = Celery(
    "arkhon",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.workers.tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
    task_soft_time_limit=3300,  # 55 minutes soft limit
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Celery Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    "fetch-feeds-daily": {
        "task": "app.workers.tasks.fetch_feeds_task",
        "schedule": 7200.0,  # Every 2 hours (in seconds)
    },
    "import-feeds-daily": {
        "task": "app.workers.tasks.import_latest_feed_task",
        "schedule": 10800.0,  # Every 3 hours
    },
    "sync-outbound-every-30min": {
        "task": "app.workers.tasks.sync_outbound_products_task",
        "schedule": 1800.0,  # Every 30 minutes
    },
}
