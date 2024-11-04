from abc import ABC, abstractmethod


class IStrategy(ABC):
    @abstractmethod
    def analyzePreviousData(self):
        pass

    @abstractmethod
    def analyzeCurrentData(self, data_points):
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
