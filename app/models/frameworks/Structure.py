from typing import Any

from app.models.asset.Candle import Candle
from app.models.frameworks.FrameWork import FrameWork


class Structure(FrameWork):

    def __init__(self, name: str, direction: str, id: Any):
        super().__init__("Structure")
        self.name: str = name
        self.direction: str = direction
        self.id = id
        self.candle = None

    def addCandle(self, candle: Candle):
        self.candle = candle

    def isIdPresent(self, ids_: list) -> bool:
        """
        Überprüft, ob der einzelne ID-Wert `self.id` in der Liste `ids_` enthalten ist.

        :param ids_: Liste von IDs, in der gesucht werden soll
        :return: True, wenn `self.id` in `ids_` enthalten ist, sonst False
        """
        return self.id in ids_
    def toDict(self) -> dict:
        """
        Converts the object to a dictionary representation.

        :return: A dictionary where the class name is the key and attributes that are not None are the value.
        """
        attributes = {
            "typ" : self.typ,
            "name": self.name,
            "direction": self.direction,
            "candles": ["" if not hasattr(self,"candle") else self.candle.toDict()],
            "ids": self.id if self.id else None,
        }

        # Filter out attributes with None values
        filtered_attributes = {key: value for key, value in attributes.items() if value is not None}

        return {self.__class__.__name__: filtered_attributes}
