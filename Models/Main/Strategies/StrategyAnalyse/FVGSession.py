from Models.Main.Strategies.ExitEntryStrategy import ExitEntryStrategy
from Models.Main.Strategies.ExpectedTimeFrame import ExpectedTimeFrame
from Models.Main.Strategies.Strategy import Strategy
from Models.StrategyAnalyse.PDArrays.FVG import FVG
from Models.StrategyAnalyse.TimeModels.London import LondonOpen


class FVGSession(Strategy,FVG):
    def __init__(self, name: str, entryStrategy : ExitEntryStrategy, exitStrategy: ExitEntryStrategy):
        super().__init__(name)
        self._TimeWindow = LondonOpen()
        self.entryStrategy = entryStrategy
        self.exitStrategy = exitStrategy
        self.safeDataDuration = 0  # Days of Data needed for StrategyAnalyse
        timeFrame = ExpectedTimeFrame(1,90)
        timeFrame2 = ExpectedTimeFrame(5,90)
        timeFrame3 = ExpectedTimeFrame(15,90)

        self.expectedTimeFrames = []

        self.expectedTimeFrames.append(timeFrame)
        self.expectedTimeFrames.append(timeFrame2)
        self.expectedTimeFrames.append(timeFrame3)

    def returnExpectedTimeFrame(self) -> list:
        return self.expectedTimeFrames

    def analyzeData(self, candles: list):
        self.getArrayList(candles)

    def isInTime(self):
        if self._TimeWindow.IsInEntryWindow() and self._TimeWindow.IsInExitWindow():
            return True
        return False

    def getEntry(self):
        pass

    def getExit(self):
        pass
