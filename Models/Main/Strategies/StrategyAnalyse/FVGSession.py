from Models.Main.Strategies.ExitEntryStrategy import ExitEntryStrategy
from Models.Main.Strategies.Strategy import Strategy
from Models.StrategyAnalyse.TimeModels.London import LondonOpen


class FVGSession(Strategy):
    def __init__(self, name: str, entryStrategy : ExitEntryStrategy, exitStrategy: ExitEntryStrategy):
        super().__init__(name)
        self._TimeWindow = LondonOpen()
        self.entryStrategy = entryStrategy
        self.exitStrategy = exitStrategy
        self.safeDataDuration = 0  # Days of Data needed for StrategyAnalyse
        self.expectedTimeFrames = [1,5,15]

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
