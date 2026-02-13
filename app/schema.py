from pydantic import BaseModel

class PredictionResponse(BaseModel):
    """Schema for the prediction response."""

    predicted_class: str
    confidence: float
