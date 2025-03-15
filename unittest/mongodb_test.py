import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
# Connect to both remote and local MongoDB instances
remote_client = MongoClient(os.getenv("MONGODBDEV"))
local_client = MongoClient(os.getenv("MONGODB"))

# Select databases and collections
remote_db = remote_client["TradingConfig"]
local_db = local_client["TradingConfig"]

remote_collection = remote_db["Asset"]
local_collection = local_db["Asset"]

# Watch for changes
with remote_collection.watch() as change_stream:
    print("Syncing changes from remote to local...")
    for change in change_stream:
        print("Change detected:", change)

        if change["operationType"] == "insert":
            local_collection.insert_one(change["fullDocument"])
        elif change["operationType"] == "update":
            local_collection.update_one(
                {"_id": change["documentKey"]["_id"]},
                {"$set": change["updateDescription"]["updatedFields"]}
            )
        elif change["operationType"] == "delete":
            local_collection.delete_one({"_id": change["documentKey"]["_id"]})