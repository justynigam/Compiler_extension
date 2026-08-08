from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.model import (
    ModelCreate,
    ModelResponse,
    ModelList,
    ModelTrainRequest,
)
from app.services.model_service import ModelService

router = APIRouter(prefix="/models", tags=["models"])


@router.post("/", response_model=ModelResponse, status_code=201)
async def create_model(
    body: ModelCreate,
    db: AsyncSession = Depends(get_db),
):
    model = await ModelService.create_model(
        db,
        name=body.name,
        model_type=body.model_type,
        description=body.description,
        config=body.config,
    )
    return ModelResponse.model_validate(model)


@router.get("/", response_model=ModelList)
async def list_models(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    models, total = await ModelService.list_models(db, skip=skip, limit=limit)
    return ModelList(
        models=[ModelResponse.model_validate(m) for m in models],
        total=total,
    )


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(model_id: int, db: AsyncSession = Depends(get_db)):
    model = await ModelService.get_model(db, model_id)
    if not model:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Model not found")
    return ModelResponse.model_validate(model)


@router.post("/{model_id}/train")
async def train_model(
    model_id: int,
    body: ModelTrainRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await ModelService.train_model(
        db,
        model_id=model_id,
        dataset_id=body.dataset_id,
        target_column=body.target_column,
        epochs=body.epochs,
    )
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/{model_id}/predict")
async def predict(
    model_id: int,
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    result = await ModelService.predict(
        db, model_id=model_id, inputs=body.get("inputs", body)
    )
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/{model_id}/explain")
async def explain(
    model_id: int,
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    result = await ModelService.explain(
        db, model_id=model_id, inputs=body.get("inputs", body)
    )
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/{model_id}/graph")
async def graph_analysis(
    model_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await ModelService.analyze_graph(db, model_id=model_id)
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.delete("/{model_id}")
async def delete_model(model_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await ModelService.delete_model(db, model_id)
    if not deleted:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Model not found")
    return {"message": "Model deleted"}