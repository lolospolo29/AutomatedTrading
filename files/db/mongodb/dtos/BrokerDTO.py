from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.db.mongodb.dtos.PyObjectId import PyObjectId


class BrokerDTO(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    brokerId: Optional[int] = None
    name: str


    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated