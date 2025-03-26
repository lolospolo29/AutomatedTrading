import uuid
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.models.PyObjectId import PyObjectId

class Trade(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id

    relation_id: Optional[str] = Field(default=None, exclude=True)
    trade_id: Optional[str] = Field(alias="tradeId", default_factory=lambda: str(uuid.uuid4()))
    category: Optional[str] = Field(default=None)
    side: Optional[str] = None
    tpsl_mode: Optional[str] = Field(default=None, alias="tpslMode")
    unrealised_pnl: Optional[str] = Field(default=None, alias="unrealisedPnl")
    leverage: Optional[str] = Field(default=None)
    size: Optional[str] = Field(default=None)
    trade_mode: Optional[int] = Field(default=None, alias="tradeMode")
    updated_time: Optional[str] = Field(default=None, alias="updatedTime")
    created_time: Optional[str] = Field(default=None, alias="createdTime")

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
