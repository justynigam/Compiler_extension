from fastapi import APIRouter
from app.api.datasets import router as datasets_router
from app.api.models import router as models_router
from app.api.predictions import router as predictions_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(datasets_router)
api_router.include_router(models_router)
api_router.include_router(predictions_router)