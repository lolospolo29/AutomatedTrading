from typing import Any

from Models.StrategyAnalyse.FrameWork import FrameWork


class Structure(FrameWork):
    def __init__(self, name: str, direction: str, id: Any):
        super().__init__("Structure")
        self.name: str = name
        self.direction: str = direction
        self.id = id
