from typing import Any

from Core.Main.Strategy.FrameWorks.FrameWork import FrameWork


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