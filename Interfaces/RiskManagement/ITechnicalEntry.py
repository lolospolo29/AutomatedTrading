from abc import ABC, abstractmethod


class ITechnicalEntry(ABC):  # Drill Fill CE
    @abstractmethod
    def getEntry(self,candle):
        pass
