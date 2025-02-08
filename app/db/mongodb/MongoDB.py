from typing import Any

from bson.objectid import ObjectId
from pymongo import MongoClient


class MongoDB:

    # region Initializing
    def __init__(self, dbName: str, uri: str):
        """
        Initialize the DbService with a MongoDB URI and database name.
        """
        self.client: Any = MongoClient(uri)
        self.db: Any = self.client[dbName]
    # endregion

    # region CRUD Standard
    def add(self, collection_name: str, data: Any) -> str:
        # """
        # Add a new document to a collection.
        # param collection_name: The name of the collection.
        # param data: A dictionary representing the document to insert.
        # :return: The inserted document's ID.
        # """
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def get(self, collection_name: str, document_id: Any) -> Any:
        """
        Retrieve a document by its ID.
        param collection_name: The name of the collection.
        param document_id: The document's unique ID (as a string).
        return: The document, or None if not found.
        """
        collection = self.db[collection_name]
        return collection.find_one({"_id": ObjectId(document_id)})

    def update(self, collection_name: str, document_id: Any, updates: Any) -> bool:
        # """
        # Update an existing document in a collection.
        # param collection_name: The name of the collection.
        # param document_id: The document's unique ID (as a string).
        # param updates: A dictionary with the fields to update.
        # return: True if the update was successful, False otherwise.
        # """
        collection = self.db[collection_name]
        result = collection.update_one({"_id": ObjectId(document_id)}, {"$set": updates})
        return result.modified_count > 0

    def delete(self, collection_name: str, document_id: Any) -> bool:
        """
        Delete a document by its ID.
        param collection_name: The name of the collection.
        param document_id: The document's unique ID (as a string).
        return: True if the deletion was successful, False otherwise.
        """
        collection = self.db[collection_name]
        result = collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count > 0
    # endregion

    # region Delete By Query, Find, Time Wise Functions
    def deleteByQuery(self, collection_name: str, query: Any) -> None:
        documents = self.find(collection_name, query)
        deletedIds = []

        for document in documents:
            documentId = str(document['_id'])
            if self.delete(collection_name, documentId):
                deletedIds.append(documentId)

    def delete_all(self, collection_name: str) -> int:
        """
        Delete all documents in the specified collection.

        param collection_name: The name of the collection.
        return: The number of documents deleted.
        """
        collection = self.db[collection_name]
        result = collection.delete_many({})

        # Return the count of deleted documents
        return result.deleted_count

    def find(self, collectionName: str, query: Any) -> list:
        """
        Find documents in a collection based on a query.
        param collection_name: The name of the collection.
        param query: A dictionary representing the query (optional).
        return: A list of matching documents.
        """
        if query is None:
            query = {}
        collection = self.db[collectionName]
        return list(collection.find(query))

    @staticmethod
    def buildQuery(attribute: str, value: Any) -> Any:
        return {f"{attribute}": value}

    def deleteOldDocuments(self, collection_name: str, date_field: Any, iso_date: Any) -> Any:
        """
        Delete documents older than a specified ISO date from the specified collection.

        :param collection_name: The name of the collection.
        :param date_field: The field name that contains the date.
        :param iso_date: The ISO date to compare against.
        :return: Number of deleted documents.
        """
        # Delete documents older than the specified ISO date
        collection = self.db[collection_name]
        result = collection.delete_many({
            date_field: {  # Use the provided date field
                '$lt': iso_date  # Less than the specified date
            }
        })

        return result.deleted_count  # Return the number of deleted documents

    def getDataWithinDateRange(self, collection_name: str, date_field: Any, start_date: Any, end_date: Any) -> list:
        """
        Retrieve data within a specified date range from the specified collection.

        :param collection_name: The name of the collection.
        :param date_field: The field name that contains the date.
        :param start_date: The start date for the range (in ISO format).
        :param end_date: The end date for the range (in ISO format).
        :return: A list of documents within the specified date range.
        """
        # Query to get documents within the specified date range
        query = {date_field: {'$gte': start_date,
                             '$lte': end_date}}  # Greater than or equal to start_date and less than or equal to
        # end_date
        collection = self.db[collection_name]
        return list(collection.find(query))
    # endregion
