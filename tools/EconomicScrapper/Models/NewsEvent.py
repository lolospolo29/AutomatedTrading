from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.models.PyObjectId import PyObjectId


class NewsEvent(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    time: datetime # 7:00 for example or 1:12
    title: str # Example:Nonfarm PayRoll
    currency:str # US
    daytime:str # AM or PM
    newEventId:int
    newsDayId:int

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated
