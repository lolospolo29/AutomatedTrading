from Models.Main.Strategies.ExitEntryStrategy import ExitEntryStrategy
from Models.Main.Strategies.ExpectedTimeFrame import ExpectedTimeFrame
from Models.Main.Strategies.Strategy import Strategy
from Models.Pattern.Mediator.ConfrimationMediator import ConfirmationMediator
from Models.Pattern.Mediator.PDMediator import PDMediator
from Models.StrategyAnalyse.TimeModels.London import LondonOpen


class FVGSession(Strategy):
    def __init__(self, name: str, entryStrategy : ExitEntryStrategy,
                 exitStrategy: ExitEntryStrategy):
        super().__init__(name)

        self._PDMediator = PDMediator()
        self._ConfirmationMediator = ConfirmationMediator()

        self._TimeWindow = LondonOpen()

        self.entryStrategy = entryStrategy
        self.exitStrategy = exitStrategy

        self.safeDataDuration = 0  # Days of Data needed for StrategyAnalyse

        timeFrame = ExpectedTimeFrame(1,20)
        timeFrame2 = ExpectedTimeFrame(5,90)
        timeFrame3 = ExpectedTimeFrame(15,90)

        self.expectedTimeFrames = []

        self.expectedTimeFrames.append(timeFrame)
        self.expectedTimeFrames.append(timeFrame2)
        self.expectedTimeFrames.append(timeFrame3)

    def returnExpectedTimeFrame(self) -> list:
        return self.expectedTimeFrames

    def analyzeData(self, candles: list):
        if len(candles) > 10:
            brk = self._PDMediator.calculatePDArray("Breaker",candles)
            swings = self._PDMediator.calculatePDArray("Swings",candles)
            vi = self._PDMediator.calculatePDArray("VolumeImbalance",candles)
            bos = self._ConfirmationMediator.calculateConfirmation("BOS",candles)
            choch = self._ConfirmationMediator.calculateConfirmation("CHOCH",candles)

    def isInTime(self):
        if self._TimeWindow.IsInEntryWindow() and self._TimeWindow.IsInExitWindow():
            return True
        return False

    def getEntry(self):
        pass

    def getExit(self):
        pass
