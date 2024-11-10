from abc import ABC, abstractmethod


class IStrategy(ABC):
    @abstractmethod
    def returnExpectedTimeFrame(self):
        pass
    @abstractmethod
    def analyzeData(self, candles: list):
        pass
    @abstractmethod
    def isInTime(self):
        pass

    @abstractmethod
    def getEntry(self):
        pass

    @abstractmethod
    def getExit(self):
        pass
