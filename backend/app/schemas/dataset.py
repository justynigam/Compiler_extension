import datetime
from pydantic import BaseModel


class DatasetBase(BaseModel):
    name: str
    description: str | None = None


class DatasetCreate(DatasetBase):
    file_path: str


class DatasetResponse(DatasetBase):
    id: int
    file_path: str
    row_count: int
    column_count: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class DatasetList(BaseModel):
    datasets: list[DatasetResponse]
    total: int