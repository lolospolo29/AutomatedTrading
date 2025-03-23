from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.models.PyObjectId import PyObjectId


class Broker(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    broker_id: int = Field(alias="brokerId")
    name: str

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated