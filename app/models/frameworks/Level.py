from app.models.frameworks.FrameWork import FrameWork


class Level(FrameWork):
    def __init__(self, name: str, level: float):
        super().__init__("Level")
        self.name: str = name
        self.direction: str = ""
        self.level: float = level
        self.fibLevel: float = 0.0
        self.ids: list= []
        self.candles = []

    def setFibLevel(self, fibLevel: float, direction: str, ids: list):
        self.fibLevel = fibLevel
        self.direction = direction
        for id in ids:
            self.ids.append(id)

    def addCandles(self, candles) -> None:
        # Efficiently add multiple candles
        self.candles.extend(candles)

    def isIdPresent(self, ids_: list) -> bool:
        """
        Überprüft, ob alle IDs in `self. Ids` in der Liste `ids_` enthalten sind.

        :param ids_: Liste von IDs, in der gesucht werden soll
        :return: True, wenn alle IDs von `self. Ids` in `ids_` enthalten sind, sonst False
        """
        return all(id_ in ids_ for id_ in self.ids)

    def toDict(self) -> dict:
        """
        Converts the object to a dictionary representation.

        :return: A dictionary where the class name is the key and attributes that are not None are the value.
        """
        attributes = {
            "typ" : self.typ,
            "name": self.name,
            "direction": self.direction,
            "ids": self.ids if self.ids else None,
            "level": self.level if self.level else None,
            "candles": [candle.toDict() for candle in self.candles],
            "fibLevel": self.fibLevel if self.fibLevel else None,
        }

        # Filter out attributes with None values
        filtered_attributes = {key: value for key, value in attributes.items() if value is not None}

        return {self.__class__.__name__: filtered_attributes}
