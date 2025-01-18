from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.FrameWork import FrameWork


class Level(FrameWork):
    def __init__(self, name: str, level: float):
        super().__init__("Level")
        self.name: str = name
        self.direction: str = ""
        self.level: float = level
        self.fib_level: float = 0.0
        self.candles: list[Candle]= []

    def set_fib_level(self, fibLevel: float, direction: str, candles: list[Candle]):
        self.fib_level = fibLevel
        self.direction = direction
        self.add_candles(candles)

    def add_candles(self, candles:list[Candle]) -> None:
        # Efficiently add multiple candles
        self.candles.extend(candles)

    def is_id_present(self, _ids: list) -> bool:
        """
        Überprüft, ob alle IDs in `self. Ids` in der Liste `ids_` enthalten sind.

        :param _ids: Liste von IDs, in der gesucht werden soll
        :return: True, wenn alle IDs von `self. Ids` in `ids_` enthalten sind, sonst False
        """
        candlesIds = [candle.id for candle in self.candles]
        return all(id_ in _ids for id_ in candlesIds)

    def to_dict(self) -> dict:
        """
        Converts the object to a dictionary representation.

        :return: A dictionary where the class name is the key and attributes that are not None are the value.
        """
        attributes = {
            "typ" : self.typ,
            "name": self.name,
            "direction": self.direction,
            "level": self.level if self.level else None,
            "candles": [candle.to_dict() for candle in self.candles],
            "fib_level": self.fib_level if self.fib_level else None,
        }

        # Filter out attributes with None values
        filtered_attributes = {key: value for key, value in attributes.items() if value is not None}

        return {self.__class__.__name__: filtered_attributes}
