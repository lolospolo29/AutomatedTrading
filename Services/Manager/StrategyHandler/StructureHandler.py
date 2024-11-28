from Models.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Models.StrategyAnalyse.Structure import Structure


class StructureHandler:
    def __init__(self):
        self.structures: list[Structure] = []

    def addStructure(self, newStructure: Structure) -> None:
        for structure in self.structures:
            if self.compareStructure(newStructure, structure):
                return
        self.structures.append(newStructure)

    def returnStructure(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        structures = []
        for structure in self.structures:
            if structure.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                structures.append(structure)
        return structures

    def removeStructure(self, _ids: list, assetBrokerStrategyRelation: AssetBrokerStrategyRelation,
                        timeFrame: int) -> None:
        structures = self.structures.copy()
        for structure in structures:
            if (structure.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation) and
                    structure.timeFrame == timeFrame):
                if not structure.isIdPresent(_ids):
                    self.structures.remove(structure)

    @staticmethod
    def compareStructure(structure1: Structure, structure2: Structure) -> bool:
        if (structure1.assetBrokerStrategyRelation.compare(structure2.assetBrokerStrategyRelation) and
                structure1.name == structure2.name and structure1.id == structure2.id
                and structure1.direction == structure2.direction):
            return True
        return False