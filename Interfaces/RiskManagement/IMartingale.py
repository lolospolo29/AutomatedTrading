from abc import ABC, abstractmethod


class IMartingale(ABC):
    @abstractmethod
    def getMartingaleModel(self,pnl):
        pass
    @abstractmethod
    def getOrderAmount(self, ratio: int ,mode :int):
        pass
