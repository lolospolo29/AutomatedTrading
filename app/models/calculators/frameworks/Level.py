from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.FrameWork import FrameWork


class Level(FrameWork):
    def __init__(self, name: str, level: float):
        super().__init__("Level")
        self.name: str = name
        self.direction: str = ""
        self.level: float = level
        self.fibLevel: float = 0.0
        self.candles: list[Candle]= []

    def setFibLevel(self, fibLevel: float, direction: str, candles: list[Candle]):
        self.fibLevel = fibLevel
        self.direction = direction
        self.addCandles(candles)

    def addCandles(self, candles:list[Candle]) -> None:
        # Efficiently add multiple candles
        self.candles.extend(candles)

    def isIdPresent(self, _ids: list) -> bool:
        """
        Überprüft, ob alle IDs in `self. Ids` in der Liste `ids_` enthalten sind.

        :param _ids: Liste von IDs, in der gesucht werden soll
        :return: True, wenn alle IDs von `self. Ids` in `ids_` enthalten sind, sonst False
        """
        candlesIds = [candle.id for candle in self.candles]
        return all(id_ in _ids for id_ in candlesIds)

    def toDict(self) -> dict:
        """
        Converts the object to a dictionary representation.

        :return: A dictionary where the class name is the key and attributes that are not None are the value.
        """
        attributes = {
            "typ" : self.typ,
            "name": self.name,
            "direction": self.direction,
            "level": self.level if self.level else None,
            "candles": [candle.toDict() for candle in self.candles],
            "fibLevel": self.fibLevel if self.fibLevel else None,
        }

        # Filter out attributes with None values
        filtered_attributes = {key: value for key, value in attributes.items() if value is not None}

        return {self.__class__.__name__: filtered_attributes}
