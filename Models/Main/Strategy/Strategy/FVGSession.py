from Interfaces.Strategy.IStrategy import IStrategy
from Models.StrategyAnalyse.TimeModels.London import LondonOpen


class FVGSession(IStrategy):
    def __init__(self, name: str, exitStrategy, entryStrategy):
        self.name: str = name
        self._TimeWindow = LondonOpen()
        self.safeDataDuration = 0  # Days of Data needed for Strategy
        self.exitStrategy = exitStrategy
        self.entryStrategy = entryStrategy
        # self.entryStrategy.setCallback(self.updatePDArrays)

    def analyzePreviousData(self, dataPoints):
        pass

    def analyzeCurrentData(self, dataPoints):
        pass

    def isInTime(self):
        if self._TimeWindow.IsInEntryWindow() and self._TimeWindow.IsInExitWindow():
            return True
        return False

    def getEntry(self):
        pass

    def getExit(self):
        pass
