import uuid
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from files.models.PyObjectId import PyObjectId

class StrategyDTO(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    name: str
    strategy_id: int = Field(alias="strategyId", default_factory=lambda: uuid.uuid4().__str__())
    entry_strategy_id: int = Field(alias="entryStrategyId")
    exit_strategy_id: int = Field(alias="exitStrategyId")

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated
