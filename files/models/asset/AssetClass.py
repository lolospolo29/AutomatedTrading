from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.models.PyObjectId import PyObjectId


class AssetClass(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    name: str
    asset_class_id: int = Field(alias="assetClassId")

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated