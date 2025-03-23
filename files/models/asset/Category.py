from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from files.models.PyObjectId import PyObjectId

class Category(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # MongoDB _id
    name: str=None
    category_id: int = Field(alias="categoryId")

    class Config:
        json_encoders = {ObjectId: str}  # Convert ObjectId to str in JSON
        populate_by_name = True  # Allow alias `_id` to be populated