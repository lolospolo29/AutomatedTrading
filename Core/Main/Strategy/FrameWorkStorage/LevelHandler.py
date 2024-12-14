from Core.Main.Asset.SubModels.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from Core.Main.Strategy.FrameWorks.Level import Level


class LevelHandler:
    def __init__(self):
        self.levels: list[Level] = []

    def addLevel(self, newLevel: Level) -> bool:
        for level in self.levels:
            if self.compareLevels(newLevel, level):
                return False
        self.levels.append(newLevel)

    def returnLevels(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        levelList = []
        for level in self.levels:
            if level.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                levelList.append(level)
        return levelList

    def removeLevel(self, _ids, assetBrokerStrategyRelation: AssetBrokerStrategyRelation, timeFrame: int) -> None:
        levels = self.levels.copy()
        for level in levels:
            if level.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation) and level.timeFrame == timeFrame:
                if not level.isIdPresent(_ids):
                    self.levels.remove(level)

    @staticmethod
    def compareLevels(level1: Level, level2: Level) ->bool:
        if (level1.assetBrokerStrategyRelation.compare(level2.assetBrokerStrategyRelation) and
                level1.name == level2.name and
                level1.level == level2.level and
                sorted(level1.ids) == sorted(level2.ids) and
                level1.direction == level2.direction):
            return True
        return False