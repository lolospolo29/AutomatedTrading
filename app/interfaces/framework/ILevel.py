from abc import ABC, abstractmethod

from Core.Main.Asset.SubModels import Candle


class ILevel(ABC):  # Opening Gap
    @abstractmethod
    def returnLevels(self, candles: list[Candle]):  # return List of all NDOG / NWOG
        pass
