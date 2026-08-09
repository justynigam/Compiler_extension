from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.prediction import Prediction
from app.schemas.prediction import PredictionResponse

router = APIRouter(prefix="/predictions", tags=["predictions"])

from sqlalchemy import select

@router.get("/", response_model=list[PredictionResponse])
async def list_predictions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Prediction).order_by(Prediction.created_at.desc()).limit(50)
    )
    predictions = result.scalars().all()
    return [PredictionResponse.model_validate(p) for p in predictions]


@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(prediction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Prediction).where(Prediction.id == prediction_id)
    )
    prediction = result.scalar_one_or_none()
    if not prediction:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Prediction not found")
    return PredictionResponse.model_validate(prediction)