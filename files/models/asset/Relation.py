import uuid
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from files.models.PyObjectId import PyObjectId


class Relation(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    asset_id: int = Field(alias="assetId")
    broker_id: int = Field(alias="brokerId")
    strategy_id: int = Field(alias="strategyId")
    relation_id: int = Field(alias="relationId", default_factory=lambda: uuid.uuid4().__str__())
    category_id: Optional[int] = Field(alias="categoryId",default=None)

    class Config:
        frozen = True  # Making the model immutable (frozen)
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated

    def __str__(self):
        return f"{self.asset} {self.broker} {self.strategy} {self.max_trades} {self.category}"

