import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
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

# Insert a new comment
async def create_comment():
    comment = CommentModel(
        name="Alice",
        email="alice@example.com",
        movie_id=ObjectId("5f982e1b3d33e3b0a4eb1234"),  # Replace with a valid movie_id
        text="Great movie! Highly recommended."
    )
    result = await comments_collection.insert_one(comment.dict(by_alias=True))
    return result.inserted_id

# Retrieve comments for a specific movie
async def get_comments_for_movie(movie_id: str):
    cursor = comments_collection.find({"movie_id": ObjectId(movie_id)})
    comments = []
    async for comment in cursor:
        comments.append(CommentModel(**comment))
    return comments

# Main function to run the async tasks
async def main():
    # Insert a comment
    comment_id = await create_comment()
    print(f"Inserted comment with ID: {comment_id}")

    # Fetch comments for a specific movie
    movie_id = "5f982e1b3d33e3b0a4eb1234"  # Replace with a valid movie_id
    comments = await get_comments_for_movie(movie_id)
    print(f"Comments for movie {movie_id}:")
    for comment in comments:
        print(comment)

# Run the event loop
asyncio.run(main())
