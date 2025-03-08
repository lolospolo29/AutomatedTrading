from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.db.mongodb.dtos.PyObjectId import PyObjectId


class RelationDTO(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    assetId: Optional[int] = None
    brokerId: Optional[int] = None
    strategyId: Optional[int] = None
    maxTrades: Optional[int] = None
    relationId: Optional[int] = None


    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated