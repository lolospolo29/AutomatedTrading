from typing import Any

from pymongo import MongoClient

from files.db.Database import Database


class MongoDB(Database):



    # region Initializing
    def __init__(self, db_name: str, uri: str):
        """
        Initialize the DbService with a MongoDB URI and database name.
        """

        self.client: Any = MongoClient(uri) # localhost
        self.db: Any = self.client[db_name] # Trades
    # endregion

    # region CRUD Standard
    def add(self, collection_name: str, data: Any) -> str:
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
        return collection.find_one({"_id": document_id})

    def update(self, collection_name: str, document_id: Any, updates: Any) -> bool:
        collection = self.db[collection_name]
        result = collection.update_one({"_id": document_id}, {"$set": updates})
        return result.modified_count > 0

    def delete(self, collection_name: str, document_id: Any) -> bool:
        """
        Delete a document by its ID.
        param collection_name: The name of the collection.
        param document_id: The document's unique ID (as a string).
        return: True if the deletion was successful, False otherwise.
        """
        collection = self.db[collection_name]
        result = collection.delete_one({"_id": document_id})
        return result.deleted_count > 0
    # endregion

    # region Delete By Query, Find, Time Wise Functions
    def delete_by_query(self, collection_name: str, query: Any) -> None:
        documents = self.find(collection_name, query)
        deleted_ids = []
        for document in documents:
            documentId = str(document['_id'])
            if self.delete(collection_name, documentId):
                deleted_ids.append(documentId)

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

    def find(self, collection_name: str, query: Any) -> list:
        """
        Find documents in a collection based on a query.
        param collection_name: The name of the collection.
        param query: A dictionary representing the query (optional).
        return: A list of matching documents.
        """
        if query is None:
            query = {}
        collection = self.db[collection_name]
        return list(collection.find(query))

    @staticmethod
    def build_query(attribute: str, value: Any) -> Any:
        return {f"{attribute}": value}

    @staticmethod
    def build_query_multiple_ids(self, **kwargs):
        for field, value in kwargs.items():
            if value is not None:
                self.query[field] = value
        return self.build()

    def delete_old_documents(self, collection_name: str, date_field: Any, iso_date: Any) -> Any:
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

    def get_data_within_date_range(self, collection_name: str, date_field: Any, start_date: Any, end_date: Any) -> list:
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

    def count(self, collection: str, query: dict) -> int:
        return self.db[collection].count_documents(query)

    def distinct(self, collection_name: str, field_name: str) -> list[Any]:
        """
        Gibt eine Liste aller eindeutigen Werte für ein bestimmtes Feld in einer Sammlung zurück.

        :param collection_name: Der Name der Sammlung.
        :param field_name: Der Name des Feldes, für das eindeutige Werte abgerufen werden sollen.
        :return: Eine Liste mit eindeutigen Werten.
        """
        collection = self.db[collection_name]
        return collection.distinct(field_name)

    def aggregate(self, collection_name: str, pipeline: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Führe eine Aggregation in der angegebenen Sammlung aus.

        :param collection_name: Name der Sammlung.
        :param pipeline: Die Aggregations-Pipeline.
        :return: Liste der aggregierten Ergebnisse.
        """
        collection = self.db[collection_name]
        return list(collection.aggregate(pipeline))
    # endregion
