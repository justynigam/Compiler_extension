import datetime
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    model_id: int
    inputs: dict


class PredictionResponse(BaseModel):
    id: int
    model_id: int
    input_data: str
    prediction: str
    confidence: float | None = None
    shap_explanation: str | None = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class ExplainabilityResponse(BaseModel):
    feature_importances: dict
    shap_graph_path: str | None = None
    lime_explanation: str | None = None