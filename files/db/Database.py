from abc import ABC, abstractmethod
from typing import List, Dict, Any


class Database(ABC):

    @abstractmethod
    def find(self, collection_or_table: str, query: dict) -> List[Dict[str, Any]]:
        """
        Find entries in the database based on a query.
        For MongoDB: this would be a document-based search.
        For SQL: this would be a table-based search.
        """
        pass

    @staticmethod
    def build_query(attribute: str, value: Any) -> Any:
        pass

    @abstractmethod
    def add(self, collection_or_table: str, entry: dict) -> None:
        """
        Add a new entry to the database.
        For MongoDB: inserts a document.
        For SQL: inserts a row into a table.
        """
        pass

    @abstractmethod
    def update(self, collection_or_table: str, entry_id: str, entry: dict) -> None:
        """
        Update an entry in the database.
        For MongoDB: updates a document.
        For SQL: updates a row.
        """
        pass

    @abstractmethod
    def delete(self, collection_or_table: str, entry_id: str) -> None:
        """
        Delete an entry from the database.
        For MongoDB: deletes a document.
        For SQL: deletes a row.
        """
        pass

    @abstractmethod
    def count(self, collection_or_table: str, query: dict) -> int:
        """
        Count the number of records based on a query.
        For MongoDB: counts the documents matching the query.
        For SQL: counts the rows based on the query.
        """
        pass
