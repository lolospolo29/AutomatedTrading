import uuid

from pydantic import BaseModel


class FrameWork(BaseModel):
    name:str=None
    id: str = str(uuid.uuid4())
    timeframe:int = None
    direction:str=None
    orderLinkId:str=None
