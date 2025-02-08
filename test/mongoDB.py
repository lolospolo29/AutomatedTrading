from motor.motor_asyncio import AsyncIOMotorClient
from pydantictest import BaseModel, Field
from bson import ObjectId

# Define a Pydantic model for the `comments` collection
class CommentModel(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    name: str
    email: str
    movie_id: ObjectId
    text: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# Connect to MongoDB
client = AsyncIOMotorClient('mongodb+srv://lauris:TF95s8wvITW3Dha9@bot.lhmav.mongodb.net/')
db = client.sample_mflix  # Access the `sample_mflix` database
comments_collection = db.comments  # Access the `comments` collection


# Retrieve comments for a specific movie
async def get_comments_for_movie(movie_id: str):
    cursor = comments_collection.find({"movie_id": ObjectId(movie_id)})
    comments = []
    async for comment in cursor:
        comments.append(CommentModel(**comment))
    return comments
