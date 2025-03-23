import uuid
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from files.models.PyObjectId import PyObjectId


class SMTPair(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    smt_pair_id: int = Field(alias="smtPairId", default_factory=lambda: uuid.uuid4().__str__())
    strategy_id: int = Field(alias="_id")
    asset_a_id: int = Field(alias="assetAId")
    asset_b_id: int = Field(alias="assetBId")
    correlation: Optional[int] = Field(alias="correlation", default=None)

    class Config:
        frozen = True
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated