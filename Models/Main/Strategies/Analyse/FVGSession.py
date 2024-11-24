from Models.Main.Strategies.ExpectedTimeFrame import ExpectedTimeFrame
from Models.Main.Strategies.Strategy import Strategy
from Models.Pattern.Mediator.ConfrimationMediator import ConfirmationMediator
from Models.Pattern.Mediator.LevelMediator import LevelMediator
from Models.Pattern.Mediator.PDMediator import PDMediator
from Models.StrategyAnalyse.Level import Level
from Models.StrategyAnalyse.PDArray import PDArray
from Models.StrategyAnalyse.Structure import Structure
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
                fvg = self._PDMediator.calculatePDArray("FVG", candles,lookback=3)
                swings = self._PDMediator.calculatePDArray("Swings", candles,lookback=3)
                ote = self._LevelMediator.calculateLevels("OTE",candles,lookback=15)

                if len(bos) > 0 or len(fvg) > 0 or len(swings) > 0:
                    frameWorks.extend(bos)
                    frameWorks.extend(fvg)
                    frameWorks.extend(swings)

            if timeFrame == 1:
                choch = self._ConfirmationMediator.calculateConfirmation("CHOCH", candles)
                fvg = self._PDMediator.calculatePDArray("FVG", candles,lookback=3)

                if len(choch) > 0  or len(fvg) > 0:
                    frameWorks.extend(choch)
                    frameWorks.extend(fvg)

        return frameWorks

    def isInTime(self):
        if self._TimeWindow.IsInEntryWindow() and self._TimeWindow.IsInExitWindow():
            return True
        return False

    def getEntry(self, candles: list, timeFrame: int, pds: list[PDArray],
                 levels:list[Level], structures: list[Structure]):
        if candles and pds and structures:
            if timeFrame == 1 and len(candles) > 10:

                latest_structures = {}

                for structure in structures:
                    latest_structures[structure.timeFrame] = structure

                fifteenMStructure = latest_structures.get(15, "")
                oneMStructures = latest_structures.get(1, "")

                if fifteenMStructure == "" or oneMStructures == "":
                    return

                fifteenMDirectionPDs = []
                oneMDirectionPDs = []
                direction = ""
                if fifteenMStructure.direction == "Bullish" and oneMStructures.direction == "Bullish":
                    direction = "Bullish"

                if fifteenMStructure.direction == "Bearish" and oneMStructures.direction == "Bearish":
                    direction = "Bearish"

                if direction == "":
                    return

                for pd in pds:
                    if pd.direction == direction:
                        if pd.timeFrame == 1:
                            oneMDirectionPDs.append(pd)
                        if pd.timeFrame == 15:
                            fifteenMDirectionPDs.append(pd)
                last_candle = candles[-1]

    def getExit(self):
        pass
