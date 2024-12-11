from Core.Main.Asset.Candle import Candle
from Core.Main.Strategies.ExpectedTimeFrame import ExpectedTimeFrame
from Core.Main.Strategies.Strategy import Strategy
from Core.Pattern.Mediator.ConfrimationMediator import ConfirmationMediator
from Core.Pattern.Mediator.LevelMediator import LevelMediator
from Core.Pattern.Mediator.PDMediator import PDMediator
from Core.StrategyAnalyse.Level import Level
from Core.StrategyAnalyse.PDArray import PDArray
from Core.StrategyAnalyse.Structure import Structure
from Core.StrategyAnalyse.TimeModels.London import LondonOpen
from Core.StrategyAnalyse.TimeModels.NYOpen import NYOpen


class FirstStrategy(Strategy):
    def __init__(self, name: str):
        super().__init__(name,False,0)

        self._PDMediator = PDMediator()
        self._ConfirmationMediator = ConfirmationMediator()
        self._LevelMediator = LevelMediator()

        self._TimeWindow = LondonOpen()
        self._TimeWindow2 = NYOpen()

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

                if len(bos) > 0 or len(fvg) > 0:
                    frameWorks.extend(bos)
                    frameWorks.extend(fvg)

            if timeFrame == 1:

                last_candle = candles[-1]
                time = last_candle.isoTime

                if self.isInTime(time):
                    fvg = self._PDMediator.calculatePDArray("FVG", candles, lookback=3)
                    frameWorks.extend(fvg)

                choch = self._ConfirmationMediator.calculateConfirmation("CHOCH", candles)

                if len(choch) > 0:
                    frameWorks.extend(choch)

        return frameWorks

    def getEntry(self, candles: list, timeFrame: int, pds: list[PDArray],
                 levels:list[Level], structures: list[Structure]):
        if candles and pds and structures:

            last_candle: Candle = candles[-1]
            time = last_candle.isoTime

            if not self.isInTime(time):
                return

            if timeFrame == 1 and len(candles) > 10:

                latest_structures = {}

                for structure in structures:
                    latest_structures[structure.timeFrame] = structure

                fifteenMStructure = latest_structures.get(15, "")
                oneMStructures = latest_structures.get(1, "")

                if fifteenMStructure == "" or oneMStructures == "":
                    return

                direction = ""

                if fifteenMStructure.direction == "Bullish" and oneMStructures.direction == "Bearish":
                    return
                if fifteenMStructure.direction == "Bearish" and oneMStructures.direction == "Bullish":
                    pass
                if fifteenMStructure.direction == "Bullish" and oneMStructures.direction == "Bullish":
                    direction = "Bullish"

                if fifteenMStructure.direction == "Bearish" and oneMStructures.direction == "Bearish":
                    direction = "Bearish"

                if direction == "":
                    return

                fifteenMDirectionPDs = []
                oneMDirectionPDs = []

                for pd in pds:
                    if pd.direction == direction:
                        if pd.timeFrame == 1:
                            oneMDirectionPDs.append(pd)
                        if pd.timeFrame == 15:
                            fifteenMDirectionPDs.append(pd)
                if len(fifteenMDirectionPDs) <= 0 or len(oneMDirectionPDs) <= 0:
                    return

                currentFifteenMPD = None

                for pd in fifteenMDirectionPDs:
                    if pd.direction == direction and pd.name == "FVG":
                        candleRangeFifteen = self._PDMediator.returnCandleRange(pd.name,pd)
                        if candleRangeFifteen['low'] < last_candle.close < candleRangeFifteen['high']:
                            currentFifteenMPD = pd

                if currentFifteenMPD is None:
                    return

                currenOneMPD = oneMDirectionPDs[-1]

                candleRange = self._PDMediator.returnCandleRange(currenOneMPD.name, currenOneMPD)

                if direction == "Bullish" and currentFifteenMPD.direction == "Bullish":
                    if candleRange['low'] < last_candle.close < candleRange['high']:
                        return "BUY"

                if direction == "Bearish" and currentFifteenMPD.direction == "Bearish":
                    if candleRange['low'] < last_candle.close < candleRange['high']:
                        return "SELL"



    def isInTime(self,time) -> bool:
        if self._TimeWindow.IsInEntryWindow(time) or self._TimeWindow2.IsInEntryWindow(time):
            return True
        return False

    def getExit(self):
        pass
