from numpy import sort

from Models.Main.Asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Models.StrategyAnalyse.Level import Level


class LevelHandler:
    def __init__(self):
        self.levels: list[Level] = []

    def addLevel(self, newLevel: Level) -> None:
        for level in self.levels:
            if self.compareLevels(newLevel, level):
                break
            self.levels.append(level)

    def returnLevels(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        levelList = []
        for level in self.levels:
            if level.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                levelList.append(level)
        return levelList

    def removeLevel(self, _ids, assetBrokerStrategyRelation: AssetBrokerStrategyRelation):
        for level in self.levels:
            if level.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                for id in _ids:
                    if level.isIdPresent(id):
                        self.levels.remove(level)
                        continue

    @staticmethod
    def compareLevels(level1: Level, level2: Level) ->bool:
        if (level1.assetBrokerStrategyRelation.compare(level2.assetBrokerStrategyRelation) and
                level1.name == level2.name and level1.level == level2.level and sort(level1.ids) == sort(level2.ids)
                and level1.direction == level2.direction):
            return True
        return False