import threading

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Structure import Structure


class StructureHandler:

    def __init__(self):
        self.structures: list[Structure] = []
        _lock = threading.Lock()

    def addStructure(self, newStructure: Structure) -> None:
        for structure in self.structures:
            if self._compareStructure(newStructure, structure):
                return
        self.structures.append(newStructure)

    def returnStructure(self) -> list[Structure]:
        return self.structures

    def removeStructure(self, candles: list[Candle],timeFrame: int) -> None:
        _ids = [candle.id for candle in candles]
        structures = self.structures.copy()
        for structure in structures:
            if structure.timeFrame == timeFrame:
                if not structure.isIdPresent(_ids):
                    self.structures.remove(structure)

    @staticmethod
    def _compareStructure(structure1: Structure, structure2: Structure) -> bool:
        if (structure1.name == structure2.name and structure1.candle.id == structure2.candle.id
                and structure1.direction == structure2.direction):
            return True
        return False
