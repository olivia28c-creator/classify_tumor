from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    predicted_class = Column(String)
    probability = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)