import uuid
from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.models.PyObjectId import PyObjectId


class Candle(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    asset: str
    broker: str
    open: float
    high: float
    low: float
    close: float
    candle_id: Optional[str] = Field(alias="candleId", default_factory=lambda: uuid.uuid4().__str__())
    iso_time: datetime = Field(...,alias="isoTime")
    timeframe: int

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated