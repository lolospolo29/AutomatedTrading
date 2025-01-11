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
    def add(self, collectionName: str, data: Any) -> str:
        # """
        # Add a new document to a collection.
        # param collection_name: The name of the collection.
        # param data: A dictionary representing the document to insert.
        # :return: The inserted document's ID.
        # """
        collection = self.db[collectionName]
        result = collection.insert_one(data)
        return str(result.inserted_id)

    def get(self, collectionName: str, documentId: Any) -> Any:
        """
        Retrieve a document by its ID.
        param collection_name: The name of the collection.
        param document_id: The document's unique ID (as a string).
        return: The document, or None if not found.
        """
        collection = self.db[collectionName]
        return collection.find_one({"_id": ObjectId(documentId)})

    def update(self, collectionName: str, documentId: Any, updates: Any) -> bool:
        # """
        # Update an existing document in a collection.
        # param collection_name: The name of the collection.
        # param document_id: The document's unique ID (as a string).
        # param updates: A dictionary with the fields to update.
        # return: True if the update was successful, False otherwise.
        # """
        collection = self.db[collectionName]
        result = collection.update_one({"_id": ObjectId(documentId)}, {"$set": updates})
        return result.modified_count > 0

    def delete(self, collectionName: str, documentId: Any) -> bool:
        """
        Delete a document by its ID.
        param collection_name: The name of the collection.
        param document_id: The document's unique ID (as a string).
        return: True if the deletion was successful, False otherwise.
        """
        collection = self.db[collectionName]
        result = collection.delete_one({"_id": ObjectId(documentId)})
        return result.deleted_count > 0
    # endregion

    # region Delete By Query, Find, Time Wise Functions
    def deleteByQuery(self, collectionName: str, query: Any) -> None:
        documents = self.find(collectionName, query)
        deletedIds = []

        for document in documents:
            documentId = str(document['_id'])
            if self.delete(collectionName, documentId):
                deletedIds.append(documentId)

    def delete_all(self, collectionName: str) -> int:
        """
        Delete all documents in the specified collection.

        param collection_name: The name of the collection.
        return: The number of documents deleted.
        """
        collection = self.db[collectionName]
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
    def buildQuery(className: str, attribute: str, value: Any) -> Any:
        return {f"{className}.{attribute}": value}

    def deleteOldDocuments(self, collectionName: str, dateField: Any, isoDate: Any) -> Any:
        """
        Delete documents older than a specified ISO date from the specified collection.

        :param collectionName: The name of the collection.
        :param dateField: The field name that contains the date.
        :param isoDate: The ISO date to compare against.
        :return: Number of deleted documents.
        """
        # Delete documents older than the specified ISO date
        collection = self.db[collectionName]
        result = collection.delete_many({
            dateField: {  # Use the provided date field
                '$lt': isoDate  # Less than the specified date
            }
        })

        return result.deleted_count  # Return the number of deleted documents

    def getDataWithinDateRange(self, collectionName: str, dateField: Any, startDate: Any, endDate: Any) -> list:
        """
        Retrieve data within a specified date range from the specified collection.

        :param collectionName: The name of the collection.
        :param dateField: The field name that contains the date.
        :param startDate: The start date for the range (in ISO format).
        :param endDate: The end date for the range (in ISO format).
        :return: A list of documents within the specified date range.
        """
        # Query to get documents within the specified date range
        query = {dateField: {'$gte': startDate,
                             '$lte': endDate}}  # Greater than or equal to start_date and less than or equal to
        # end_date
        collection = self.db[collectionName]
        return list(collection.find(query))
    # endregion
