import threading

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.frameworks.Structure import Structure


class StructureHandler:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(StructureHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.structures: list[Structure] = []
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Add / Return Function

    def addStructure(self, newStructure: Structure) -> None:
        for structure in self.structures:
            if self._compareStructure(newStructure, structure):
                return
        self.structures.append(newStructure)

    def returnStructure(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        structures = []
        for structure in self.structures:
            if structure.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                structures.append(structure)
        return structures

    # endregion

    # region Remove / Compare Function
    def removeStructure(self, _ids: list, assetBrokerStrategyRelation: AssetBrokerStrategyRelation,
                        timeFrame: int) -> None:
        structures = self.structures.copy()
        for structure in structures:
            if (structure.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation) and
                    structure.timeFrame == timeFrame):
                if not structure.isIdPresent(_ids):
                    self.structures.remove(structure)

    @staticmethod
    def _compareStructure(structure1: Structure, structure2: Structure) -> bool:
        if (structure1.assetBrokerStrategyRelation.compare(structure2.assetBrokerStrategyRelation) and
                structure1.name == structure2.name and structure1.id == structure2.id
                and structure1.direction == structure2.direction):
            return True
        return False
    # endregion