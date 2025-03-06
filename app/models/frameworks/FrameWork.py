import uuid

from pydantic import BaseModel

from app.models.asset.Candle import Candle


class FrameWork(BaseModel):
    name:str=None
    id: str = str(uuid.uuid4())
    timeframe:int = None
    direction:str=None
    orderLinkId:str=None
    candles:list[Candle]
    status:str="Normal"
    reference:str = ""