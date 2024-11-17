from abc import ABC, abstractmethod

from Models.Main.Asset.Candle import Candle


class IRiskInvalidation(ABC):
    @abstractmethod
    def checkInvalidation(self,stopLoss: float, candle: Candle, tradeDirection: str):
        pass
