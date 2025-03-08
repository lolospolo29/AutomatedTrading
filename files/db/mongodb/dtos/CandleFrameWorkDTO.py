from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.db.mongodb.dtos.PyObjectId import PyObjectId


class CandleFrameWorkDTO(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    frameWorkId: Optional[str] = None
    asset: Optional[str] = None
    broker: Optional[str] = None
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    candleId : Optional[str] = None
    iso_time: Optional[datetime]
    timeframe: Optional[int] = None

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated