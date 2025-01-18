import threading

from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Level import Level


class LevelHandler:

    def __init__(self):
        self.levels: list[Level] = []
        _lock = threading.Lock()


    def add_level(self, new_level: Level) -> bool:
        for level in self.levels:
            if self._compare_levels(new_level, level):
                return False
        self.levels.append(new_level)
        return True

    def return_levels(self) -> list[Level]:
        return self.levels

    def remove_level(self, candles:list[Candle], timeframe: int) -> None:
        _ids = [candle.id for candle in candles]
        levels = self.levels.copy()
        for level in levels:
            if level.timeframe == timeframe:
                if not level.is_id_present(_ids):
                    self.levels.remove(level)

    @staticmethod
    def _compare_levels(level1: Level, level2: Level) -> bool:
        _1ids = [candle.id for candle in level1.candles]
        _2ids = [candle.id for candle in level2.candles]
        if (level1.name == level2.name and level1.level == level2.level and sorted(_1ids) == sorted(_2ids) and
                level1.direction == level2.direction):
            return True
        return False
