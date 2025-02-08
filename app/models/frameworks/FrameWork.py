import uuid

from pydantic import BaseModel


class FrameWork(BaseModel):
    name:str
    id: str = str(uuid.uuid4())
    timeframe:int = None
    direction:str

