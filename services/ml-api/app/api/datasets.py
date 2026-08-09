from fastapi import APIRouter, Depends, File, UploadFile, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.dataset import DatasetResponse, DatasetList
from app.services.dataset_service import DatasetService

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/", response_model=DatasetResponse, status_code=201)
async def create_dataset(
    name: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    dataset = await DatasetService.create_dataset(
        db, name=name, description=description, file_content=content, filename=file.filename
    )
    return DatasetResponse.model_validate(dataset)


@router.get("/", response_model=DatasetList)
async def list_datasets(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    datasets, total = await DatasetService.list_datasets(db, skip=skip, limit=limit)
    return DatasetList(
        datasets=[DatasetResponse.model_validate(d) for d in datasets],
        total=total,
    )


@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(dataset_id: int, db: AsyncSession = Depends(get_db)):
    dataset = await DatasetService.get_dataset(db, dataset_id)
    if not dataset:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Dataset not found")
    return DatasetResponse.model_validate(dataset)


@router.delete("/{dataset_id}")
async def delete_dataset(dataset_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await DatasetService.delete_dataset(db, dataset_id)
    if not deleted:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Dataset not found")
    return {"message": "Dataset deleted"}