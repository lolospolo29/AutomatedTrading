import uuid
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from files.models.asset.Candle import Candle
from files.models.PyObjectId import PyObjectId

class FrameWork(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    framework_id: str = Field(alias="frameworkId", default_factory=lambda: uuid.uuid4().__str__())
    name: str = None
    timeframe: int = None
    direction: str = None
    candles: list[Candle] = Field(exclude=True,default=None)
    typ:str
    status: str = Field(default="Normal")
    reference: str = Field(default="")
    invalidation_candle: Optional[Candle] = Field(exclude=True,default=None,alias="invalidationCandle")
