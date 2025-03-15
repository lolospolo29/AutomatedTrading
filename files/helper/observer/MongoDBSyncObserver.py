from pymongo import MongoClient


class MongoDBSyncObserver:
    def __init__(self, client1_uri, client2_uri, db_name, collection_name):
        """
        Initializes the MongoDBSyncWatcher with two MongoDB clients, database, and collection.

        :param client1_uri: MongoDB URI for the remote database
        :param client2_uri: MongoDB URI for the local database
        :param db_name: Database name (must be the same for both clients)
        :param collection_name: Collection name to watch
        """
        self.client1 = MongoClient(client1_uri)
        self.client2 = MongoClient(client2_uri)

        self.remote_db = self.client1[db_name]
        self.local_db = self.client2[db_name]

        self.remote_collection = self.remote_db[collection_name]
        self.local_collection = self.local_db[collection_name]

    def start_watching(self):
        """
        Starts watching the remote collection and syncs changes to the local collection.
        """
        print(f"Watching changes on collection '{self.remote_collection.name}' in database '{self.remote_db.name}'")

        with self.remote_collection.watch() as change_stream:
            for change in change_stream:
                print("Change detected:", change)

                if change["operationType"] == "insert":
                    self.local_collection.insert_one(change["fullDocument"])
                elif change["operationType"] == "update":
                    self.local_collection.update_one(
                        {"_id": change["documentKey"]["_id"]},
                        {"$set": change["updateDescription"]["updatedFields"]}
                    )
                elif change["operationType"] == "delete":
                    self.local_collection.delete_one({"_id": change["documentKey"]["_id"]})