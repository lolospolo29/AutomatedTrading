from Models.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Models.StrategyAnalyse.Structure import Structure


class StructureHandler:
    def __init__(self):
        self.structures: list[Structure] = []

    def addStructure(self, newLevel: Structure) -> None:
        for level in self.structures:
            if self.compareStructure(newLevel, level):
                break
            self.structures.append(level)

    def returnStructure(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        structures = []
        for structure in self.structures:
            if structure.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                structures.append(structure)
        return structures

    def removeStructure(self, _ids, assetBrokerStrategyRelation: AssetBrokerStrategyRelation):
        for structure in self.structures:
            if structure.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                for id in _ids:
                    if structure.id == id:
                        self.structures.remove(structure)
                        continue

    @staticmethod
    def compareStructure(structure1: Structure, structure2: Structure) -> bool:
        if (structure1.assetBrokerStrategyRelation.compare(structure2.assetBrokerStrategyRelation) and
                structure1.name == structure2.name and structure1.id == structure2.id
                and structure1.direction == structure2.direction):
            return True
        return False