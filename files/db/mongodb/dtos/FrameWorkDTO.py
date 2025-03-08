from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.db.mongodb.dtos.PyObjectId import PyObjectId


class FrameWorkDTO(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    name:Optional[str]=None
    type:Optional[str]=None
    level:Optional[float]=None
    fib_level:Optional[float]=None
    status:Optional[str]=None
    frameWorkId: Optional[str] = None
    timeframe:Optional[int] = None
    direction:Optional[str]=None
    orderLinkId:Optional[str]=None

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated