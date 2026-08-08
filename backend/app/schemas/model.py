import datetime
from pydantic import BaseModel


class ModelBase(BaseModel):
    name: str
    model_type: str
    description: str | None = None
    config: str | None = None


class ModelCreate(ModelBase):
    pass


class ModelTrainRequest(BaseModel):
    dataset_id: int
    target_column: str
    epochs: int = 10


class ModelResponse(ModelBase):
    id: int
    artifact_path: str | None = None
    accuracy: float | None = None
    f1_score: float | None = None
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


class ModelList(BaseModel):
    models: list[ModelResponse]
    total: int