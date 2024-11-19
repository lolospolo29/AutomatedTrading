from Models.Main.Strategies.ExpectedTimeFrame import ExpectedTimeFrame
from Models.Main.Strategies.Strategy import Strategy
from Models.Pattern.Mediator.ConfrimationMediator import ConfirmationMediator
from Models.Pattern.Mediator.LevelMediator import LevelMediator
from Models.Pattern.Mediator.PDMediator import PDMediator
from Models.StrategyAnalyse.TimeModels.London import LondonOpen


class FVGSession(Strategy):
    def __init__(self, name: str):
        super().__init__(name,False,0)

        self._PDMediator = PDMediator()
        self._ConfirmationMediator = ConfirmationMediator()
        self._LevelMediator = LevelMediator()

        self._TimeWindow = LondonOpen()

        self.expectedTimeFrames = []

        timeFrame = ExpectedTimeFrame(1,90)
        timeFrame2 = ExpectedTimeFrame(5,90)
        timeFrame3 = ExpectedTimeFrame(15,90)

        self.expectedTimeFrames.append(timeFrame)
        self.expectedTimeFrames.append(timeFrame2)
        self.expectedTimeFrames.append(timeFrame3)

    def returnExpectedTimeFrame(self) -> list:
        return self.expectedTimeFrames

    def analyzeData(self, candles: list, timeFrame: int) -> list:
        frameWorks = []
        if len(candles) > 10:
            if timeFrame == 15:
                bos = self._ConfirmationMediator.calculateConfirmation("BOS", candles)
                ote = self._LevelMediator.calculateLevels("OTE", candles)
                fvg = self._PDMediator.calculatePDArray("FVG", candles)
                swings = self._PDMediator.calculatePDArray("Swings", candles)

                if len(bos) > 0 or len(ote) > 0 or len(fvg) > 0 or len(swings) > 0:
                    frameWorks.extend(bos)
                    frameWorks.extend(ote)
                    frameWorks.extend(fvg)
                    frameWorks.extend(swings)

            if timeFrame == 1:
                choch = self._ConfirmationMediator.calculateConfirmation("CHOCH", candles)
                cisd = self._ConfirmationMediator.calculateConfirmation("CISD",candles)
                fvg = self._PDMediator.calculatePDArray("FVG", candles)

                if len(choch) > 0 or len(cisd) > 0 or len(fvg) > 0:
                    frameWorks.extend(choch)
                    frameWorks.extend(cisd)
                    frameWorks.extend(fvg)

        return frameWorks

    def isInTime(self):
        if self._TimeWindow.IsInEntryWindow() and self._TimeWindow.IsInExitWindow():
            return True
        return False

    def getEntry(self, candles: list, timeFrame: int, pd: list, level:list, structure: list):
        if self.isInTime():
            pass

    def getExit(self):
        pass
