from typing import Any

from Models.StrategyAnalyse.FrameWork import FrameWork


class Level(FrameWork):
    def __init__(self, name: str, level: float):
        super().__init__("Level")
        self.name: str = name
        self.direction = None
        self.level: float = level
        self.fibLevel = None
        self.ids: list= []

    def setFibLevel(self, fibLevel: float, direction: str, ids: list):
        self.fibLevel = fibLevel
        self.direction = direction
        for id in ids:
            self.ids.append(id)

    def isIdPresent(self, id_: list) -> Any:
        """
        Check if a specific ID is stored in the 'ids' list.
        """
        if id_ in self.ids:
            return True
        return False
