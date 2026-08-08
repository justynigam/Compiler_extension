import os
import json
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate as DatasetCreateSchema


class DatasetService:
    UPLOAD_DIR = "./uploads/datasets"

    @classmethod
    async def ensure_upload_dir(cls):
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)

    @classmethod
    async def create_dataset(
        cls, db: AsyncSession, name: str, description: str | None, file_content: bytes, filename: str
    ) -> Dataset:
        await cls.ensure_upload_dir()
        file_path = os.path.join(cls.UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(file_content)
        try:
            df = pd.read_csv(file_path)
            row_count, column_count = len(df), len(df.columns)
        except Exception:
            row_count, column_count = 0, 0
        dataset = Dataset(
            name=name,
            description=description,
            file_path=file_path,
            row_count=row_count,
            column_count=column_count,
        )
        db.add(dataset)
        await db.flush()
        return dataset

    @classmethod
    async def get_dataset(cls, db: AsyncSession, dataset_id: int) -> Dataset | None:
        result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
        return result.scalar_one_or_none()

    @classmethod
    async def list_datasets(
        cls, db: AsyncSession, skip: int = 0, limit: int = 50
    ) -> tuple[list[Dataset], int]:
        count_q = await db.execute(select(func.count(Dataset.id)))
        total = count_q.scalar()
        result = await db.execute(
            select(Dataset).offset(skip).limit(limit).order_by(Dataset.created_at.desc())
        )
        return result.scalars().all(), total

    @classmethod
    async def delete_dataset(cls, db: AsyncSession, dataset_id: int) -> bool:
        dataset = await cls.get_dataset(db, dataset_id)
        if not dataset:
            return False
        if os.path.exists(dataset.file_path):
            os.remove(dataset.file_path)
        await db.delete(dataset)
        return True