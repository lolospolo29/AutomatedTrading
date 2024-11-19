from typing import Any

from Models.StrategyAnalyse.FrameWork import FrameWork


class PDArray(FrameWork):
    def __init__(self, name: str, direction: str):
        super().__init__("PDArray")
        self.name: str = name
        self.direction: str = direction
        self.Ids: list = []

    def addId(self, Id: Any) -> None:
        if Id not in self.Ids:
            self.Ids.append(Id)

    def isIdPresent(self, ids_: list) -> bool:
        """
        Überprüft, ob alle IDs in `self.Ids` in der Liste `ids_` enthalten sind.

        :param ids_: Liste von IDs, in der gesucht werden soll
        :return: True, wenn alle IDs von `self.Ids` in `ids_` enthalten sind, sonst False
        """
        return all(id_ in ids_ for id_ in self.Ids)