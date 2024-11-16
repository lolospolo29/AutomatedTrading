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

    def isIdPresent(self, id_: list) -> Any:
        """
        Check if a specific ID is stored in the 'ids' list.
        """
        if id_ in self.Ids:
            return True
        return False