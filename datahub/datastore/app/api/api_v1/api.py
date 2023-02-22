from fastapi import APIRouter

from app.api.api_v1.endpoints import influx

api_router = APIRouter()
api_router.include_router(influx.router, prefix="/influx", tags=["influx"])