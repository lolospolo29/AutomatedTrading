import asyncio

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field


# Define a Pydantic model for MongoDB document
class UserModel(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    email: str
    age: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Connect to MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.test_db

async def create_user():
    user = UserModel(name="Alice", email="alice@example.com", age=30)
    # Insert the document
    result = await db.user.insert_one(user.dict(by_alias=True))
    return result.inserted_id

async def get_user():
    user_data = await db.user.find_one({"name": "Alice"})
    user = UserModel(**user_data)  # Automatically map MongoDB document to UserModel
    return user


async def main():
    await create_user()
    user = await get_user()
    print(user.age)

# Call asyncio.run() only once
asyncio.run(main())
