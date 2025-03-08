from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.db.mongodb.dtos.PyObjectId import PyObjectId


class TradeDTO(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    relationId: int = None
    tradeId: Optional[str] = None
    category: Optional[str] = None
    side: Optional[str] = None
    tpslMode: Optional[str] = None
    unrealisedPnl: Optional[str] = None
    leverage: Optional[str] = None
    size: Optional[str] = None
    tradeMode: Optional[int] = None
    updatedTime: Optional[str] = None
    createdTime: Optional[str] = None


    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated