import threading

from app.models.asset.AssetBrokerStrategyRelation import AssetBrokerStrategyRelation
from app.models.asset.Candle import Candle
from app.models.frameworks.Level import Level


class LevelHandler:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(LevelHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    # region Initializing
    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prüfe, ob bereits initialisiert
            self.levels: list[Level] = []
            self._initialized = True  # Markiere als initialisiert

    # endregion

    # region Add / Return Function
    def addLevel(self, newLevel: Level) -> bool:
        for level in self.levels:
            if self._compareLevels(newLevel, level):
                return False
        self.levels.append(newLevel)
        return True

    def returnLevels(self, assetBrokerStrategyRelation: AssetBrokerStrategyRelation) -> list:
        levelList = []
        for level in self.levels:
            if level.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation):
                levelList.append(level)
        return levelList
    # endregion

    def addCandleByIds(self, candles: list[Candle], timeFrame: int,
                       assetBrokerStrategyRelation: AssetBrokerStrategyRelation)-> None:
        for level in self.levels:
            if level.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation) and level.timeFrame == timeFrame:

                existing_ids = {candle.id for candle in level.candles}  # Cache existing IDs
                new_candles = [
                    candle for candle in candles
                    if candle.id in level.Ids and candle.id not in existing_ids
                ]

                # Assuming pd.addCandles accepts a list of candles
                if new_candles:
                    level.addCandles(new_candles)

    # region Compare and Remove
    def removeLevel(self, _ids, assetBrokerStrategyRelation: AssetBrokerStrategyRelation, timeFrame: int) -> None:
        levels = self.levels.copy()
        for level in levels:
            if level.assetBrokerStrategyRelation.compare(assetBrokerStrategyRelation) and level.timeFrame == timeFrame:
                if not level.isIdPresent(_ids):
                    self.levels.remove(level)

    @staticmethod
    def _compareLevels(level1: Level, level2: Level) ->bool:
        if (level1.assetBrokerStrategyRelation.compare(level2.assetBrokerStrategyRelation) and
                level1.name == level2.name and
                level1.level == level2.level and
                sorted(level1.ids) == sorted(level2.ids) and
                level1.direction == level2.direction):
            return True
        return False
    # endregion