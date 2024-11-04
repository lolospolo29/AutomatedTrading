from abc import ABC, abstractmethod

from Models.Asset import Candle


class ILevel(ABC):  # Opening Gap
    @abstractmethod
    def getLevels(self, candles: list[Candle]):  # return List of all NDOG / NWOG
        pass
