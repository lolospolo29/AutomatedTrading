from abc import ABC, abstractmethod

from Core.Main.Asset.SubModels.Candle import Candle


class IRiskInvalidation(ABC):
    @abstractmethod
    def checkInvalidation(self,stopLoss: float, candle: Candle, tradeDirection: str):
        pass
