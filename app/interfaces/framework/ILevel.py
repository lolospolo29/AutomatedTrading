from abc import ABC, abstractmethod

from app.models.asset.Candle import Candle


class ILevel(ABC):  # Opening Gap
    @abstractmethod
    def returnLevels(self, candles: list[Candle]):  # return List of all NDOG / NWOG
        pass
