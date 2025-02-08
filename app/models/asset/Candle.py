import uuid
from datetime import datetime

from pydantic import BaseModel,Field


class Candle(BaseModel):

    asset: str
    broker: str
    open: float
    high: float
    low: float
    close: float
    iso_time: datetime
    timeframe: int
    id: str = Field(default=str(uuid.uuid4()))
