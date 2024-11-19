from abc import ABC, abstractmethod


class IStrategy(ABC):
    @abstractmethod
    def returnExpectedTimeFrame(self):
        pass
    @abstractmethod
    def analyzeData(self, candles: list, timeFrame: int) -> list:
        pass
    @abstractmethod
    def isInTime(self):
        pass

    @abstractmethod
    def getEntry(self, candles: list, timeFrame: int, pd: list, level:list, structure: list):
        pass

    @abstractmethod
    def getExit(self):
        pass
