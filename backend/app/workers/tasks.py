"""Celery tasks for background processing."""
import logging
import json
from datetime import datetime
from decimal import Decimal
from sqlalchemy import select

from app.workers.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.feed import InboundFeed, FeedStatus
from app.models.outbound import OutboundJob, OutboundStatus
from app.models.product import Product
from app.services.ftp_service import FTPService
from app.services.import_service import ImportService


logger = logging.getLogger(__name__)


@celery_app.task(name="app.workers.tasks.fetch_feeds_task")
def fetch_feeds_task():
    """Fetch product feeds from FTP servers."""
    import asyncio
    return asyncio.run(_fetch_feeds_async())


async def _fetch_feeds_async():
    """Async implementation of fetch feeds."""
    try:
        entities = ["bigbuy"]  # In production, load from config/database

        results = []
        for entity_code in entities:
            try:
                ftp_service = FTPService(entity_code)

                # List files
                files = await ftp_service.list_files(pattern="products")

                # Download latest file
                if files:
                    latest_file = sorted(files, key=lambda x: x.get("modified", ""), reverse=True)[0]
                    local_path = await ftp_service.download_feed(latest_file["name"])

                    if local_path:
                        # Create feed record
                        async with AsyncSessionLocal() as db:
                            feed = InboundFeed(
                                entity_code=entity_code,
                                file_name=latest_file["name"],
                                file_path=local_path,
                                file_size=latest_file.get("size", 0),
                                status=FeedStatus.PENDING
                            )
                            db.add(feed)
                            await db.commit()

                            results.append({
                                "entity": entity_code,
                                "file": latest_file["name"],
                                "feed_id": feed.id,
                                "status": "success"
                            })
                    else:
                        results.append({
                            "entity": entity_code,
                            "status": "download_failed"
                        })
                else:
                    results.append({
                        "entity": entity_code,
                        "status": "no_files"
                    })

            except Exception as e:
                logger.error(f"Fetch failed for {entity_code}: {e}")
                results.append({
                    "entity": entity_code,
                    "status": "error",
                    "error": str(e)
                })

        return {
            "task": "fetch_feeds",
            "timestamp": datetime.utcnow().isoformat(),
            "results": results
        }

    except Exception as e:
        logger.error(f"Fetch feeds task failed: {e}", exc_info=True)
        return {
            "task": "fetch_feeds",
            "status": "failed",
            "error": str(e)
        }


@celery_app.task(name="app.workers.tasks.import_latest_feed_task")
def import_latest_feed_task():
    """Import the latest pending feed."""
    import asyncio
    return asyncio.run(_import_latest_feed_async())


async def _import_latest_feed_async():
    """Async implementation of import latest feed."""
    try:
        async with AsyncSessionLocal() as db:
            # Find latest pending feed
            result = await db.execute(
                select(InboundFeed)
                .where(InboundFeed.status == FeedStatus.PENDING)
                .order_by(InboundFeed.created_at.desc())
                .limit(1)
            )
            feed = result.scalar_one_or_none()

            if not feed:
                return {
                    "task": "import_latest_feed",
                    "status": "no_pending_feeds"
                }

            # Import feed
            import_service = ImportService(db, feed.id)
            success = await import_service.import_feed()

            return {
                "task": "import_latest_feed",
                "feed_id": feed.id,
                "status": "success" if success else "failed",
                "timestamp": datetime.utcnow().isoformat()
            }

    except Exception as e:
        logger.error(f"Import task failed: {e}", exc_info=True)
        return {
            "task": "import_latest_feed",
            "status": "failed",
            "error": str(e)
        }


@celery_app.task(name="app.workers.tasks.import_feed_task")
def import_feed_task(feed_id: int):
    """Import a specific feed."""
    import asyncio
    return asyncio.run(_import_feed_async(feed_id))


async def _import_feed_async(feed_id: int):
    """Async implementation of import feed."""
    try:
        async with AsyncSessionLocal() as db:
            import_service = ImportService(db, feed_id)
            success = await import_service.import_feed()

            return {
                "task": "import_feed",
                "feed_id": feed_id,
                "status": "success" if success else "failed"
            }

    except Exception as e:
        logger.error(f"Import feed {feed_id} failed: {e}", exc_info=True)
        return {
            "task": "import_feed",
            "feed_id": feed_id,
            "status": "failed",
            "error": str(e)
        }


@celery_app.task(name="app.workers.tasks.process_bulk_update")
def process_bulk_update(job_id: int):
    """Process bulk update job."""
    import asyncio
    return asyncio.run(_process_bulk_update_async(job_id))


async def _process_bulk_update_async(job_id: int):
    """Async implementation of bulk update."""
    try:
        async with AsyncSessionLocal() as db:
            # Get job
            result = await db.execute(
                select(OutboundJob).where(OutboundJob.id == job_id)
            )
            job = result.scalar_one_or_none()

            if not job:
                return {"status": "job_not_found"}

            # Update status
            job.status = OutboundStatus.PROCESSING
            job.started_at = datetime.utcnow()
            await db.commit()

            # Parse bulk data
            bulk_data = json.loads(job.bulk_data)
            target_field = bulk_data["target_field"]

            # Apply updates
            success_count = 0
            error_count = 0

            for change in bulk_data["changes"]:
                try:
                    product_id = change["product_id"]
                    new_value = Decimal(change["new_value"])

                    result = await db.execute(
                        select(Product).where(Product.id == product_id)
                    )
                    product = result.scalar_one_or_none()

                    if product:
                        setattr(product, target_field, new_value)
                        success_count += 1

                except Exception as e:
                    logger.error(f"Update failed for product {change.get('product_id')}: {e}")
                    error_count += 1

            await db.commit()

            # Update job status
            job.success_count = success_count
            job.error_count = error_count
            job.status = OutboundStatus.COMPLETED if error_count == 0 else OutboundStatus.PARTIAL
            job.completed_at = datetime.utcnow()
            job.message = f"Updated {success_count} products"
            await db.commit()

            return {
                "task": "process_bulk_update",
                "job_id": job_id,
                "success_count": success_count,
                "error_count": error_count,
                "status": "success"
            }

    except Exception as e:
        logger.error(f"Bulk update job {job_id} failed: {e}", exc_info=True)

        # Update job status
        try:
            async with AsyncSessionLocal() as db:
                result = await db.execute(
                    select(OutboundJob).where(OutboundJob.id == job_id)
                )
                job = result.scalar_one_or_none()
                if job:
                    job.status = OutboundStatus.FAILED
                    job.message = str(e)
                    job.completed_at = datetime.utcnow()
                    await db.commit()
        except:
            pass

        return {
            "task": "process_bulk_update",
            "job_id": job_id,
            "status": "failed",
            "error": str(e)
        }


@celery_app.task(name="app.workers.tasks.sync_outbound_products_task")
def sync_outbound_products_task():
    """Sync pending outbound products."""
    import asyncio
    return asyncio.run(_sync_outbound_async())


async def _sync_outbound_async():
    """Async implementation of outbound sync."""
    try:
        async with AsyncSessionLocal() as db:
            # Find pending outbound jobs
            result = await db.execute(
                select(OutboundJob)
                .where(OutboundJob.status == OutboundStatus.PENDING)
                .order_by(OutboundJob.created_at)
                .limit(10)
            )
            jobs = result.scalars().all()

            if not jobs:
                return {
                    "task": "sync_outbound_products",
                    "status": "no_pending_jobs"
                }

            results = []
            for job in jobs:
                # Process each job (implement actual sync logic here)
                # This is a placeholder - in production, call actual outbound APIs

                job.status = OutboundStatus.PROCESSING
                await db.commit()

                # Simulate processing
                job.status = OutboundStatus.COMPLETED
                job.completed_at = datetime.utcnow()
                job.message = "Synced successfully"

                results.append({
                    "job_id": job.id,
                    "sync_id": job.sync_id,
                    "status": "synced"
                })

            await db.commit()

            return {
                "task": "sync_outbound_products",
                "processed": len(results),
                "results": results,
                "timestamp": datetime.utcnow().isoformat()
            }

    except Exception as e:
        logger.error(f"Outbound sync task failed: {e}", exc_info=True)
        return {
            "task": "sync_outbound_products",
            "status": "failed",
            "error": str(e)
        }
