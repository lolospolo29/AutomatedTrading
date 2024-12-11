from typing import Any

from Core.StrategyAnalyse.FrameWork import FrameWork


class Structure(FrameWork):
    def __init__(self, name: str, direction: str, id: Any):
        super().__init__("Structure")
        self.name: str = name
        self.direction: str = direction
        self.id = id

    def isIdPresent(self, ids_: list) -> bool:
        """
        Überprüft, ob der einzelne ID-Wert `self.id` in der Liste `ids_` enthalten ist.

        :param ids_: Liste von IDs, in der gesucht werden soll
        :return: True, wenn `self.id` in `ids_` enthalten ist, sonst False
        """
        return self.id in ids_
