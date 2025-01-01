from typing import Any, overload

from app.models.frameworks.FrameWork import FrameWork


class PDArray(FrameWork):
    def __init__(self, name: str, direction: str):
        super().__init__("PDArray")
        self.name: str = name
        self.direction: str = direction
        self.Ids: set = set()  # Use a set for faster lookup
        self.candles = []
        self.status = ""

    def addId(self, Id: Any) -> None:
        # Add a single ID if not already present
        self.Ids.add(Id)

    def addCandles(self, candles) -> None:
        # Efficiently add multiple candles
        self.candles.extend(candles)

    def addStatus(self, status) -> None:
        self.status = status

    def isIdPresent(self, ids_: list) -> bool:
        """
        Überprüft, ob alle IDs in `self.Ids` in der Liste `ids_` enthalten sind.

        :param ids_: Liste von IDs, in der gesucht werden soll
        :return: True, wenn alle IDs von `self.Ids` in `ids_` enthalten sind, sonst False
        """
        return all(id_ in ids_ for id_ in self.Ids)

    def toDict(self) -> dict:
        """
        Converts the object to a dictionary representation.

        :return: A dictionary where the class name is the key and attributes that are not None are the value.
        """
        attributes = {
            "typ" : self.typ,
            "timeFrame" : self.timeFrame,
            "name": self.name,
            "direction": self.direction,
            "Ids": list(self.Ids) if self.Ids else None,
            "candles": self.candles if self.candles else None,
            "status": self.status if self.status else None,
        }

        # Filter out attributes with None values
        filtered_attributes = {key: value for key, value in attributes.items() if value is not None}

        return {self.__class__.__name__: filtered_attributes}
