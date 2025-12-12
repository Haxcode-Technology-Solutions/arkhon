"""API v1 router."""
from fastapi import APIRouter

from app.api.v1 import auth, dashboard, feeds, products, outbound, manufacturers, categories, attributes, logs, settings, cron


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(feeds.router, prefix="/feeds", tags=["Feeds"])
api_router.include_router(outbound.router, prefix="/outbound", tags=["Outbound"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(manufacturers.router, prefix="/manufacturers", tags=["Manufacturers"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(attributes.router, prefix="/attributes", tags=["Attributes"])
api_router.include_router(logs.router, prefix="/logs", tags=["Logs"])
api_router.include_router(settings.router, prefix="/settings", tags=["Settings"])
api_router.include_router(cron.router, prefix="/cron", tags=["Cron"])
