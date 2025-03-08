import uuid

from pydantic import BaseModel,Field

from files.models.asset.Candle import Candle


class FrameWork(BaseModel):
    name: str = None
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # Generates a new UUID per instance
    timeframe: int = None
    direction: str = None
    orderLinkId: str = None
    candles: list[Candle]
    status: str = "Normal"
    reference: str = ""
    invalidation_candle: Candle = None