from app.models.asset.Candle import Candle
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.Strategy import Strategy
from app.helper.mediator.StructureMediator import StructureMediator
from app.helper.mediator.LevelMediator import LevelMediator
from app.helper.mediator.PDMediator import PDMediator
from app.models.calculators.frameworks.Level import Level
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.frameworks.Structure import Structure
from app.models.calculators.frameworks.time.London import LondonOpen
from app.models.calculators.frameworks.time.NYOpen import NYOpen


class FVGSession(Strategy):
    def __init__(self):
        name:str = "FVG"
        super().__init__(name,False)

        self._PDMediator = PDMediator()
        self._ConfirmationMediator = StructureMediator()
        self._LevelMediator : LevelMediator= LevelMediator()

        self._TimeWindow = LondonOpen()
        self._TimeWindow2 = NYOpen()

        self.expectedTimeFrames = []

        timeFrame = ExpectedTimeFrame(1,90)
        timeFrame2 = ExpectedTimeFrame(5,90)
        timeFrame3 = ExpectedTimeFrame(15,90)
        timeFrame4 = ExpectedTimeFrame(240,1)

        self.expectedTimeFrames.append(timeFrame)
        self.expectedTimeFrames.append(timeFrame2)
        self.expectedTimeFrames.append(timeFrame3)
        self.expectedTimeFrames.append(timeFrame4)


    def isInTime(self,time) -> bool:
        if self._TimeWindow.IsInEntryWindow(time) or self._TimeWindow2.IsInEntryWindow(time):
            return True
        return False

    def _analyzeData(self, candles: list, timeFrame: int) -> list:
            frameWorks = []
            last_candle = candles[-1]
            time = last_candle.isoTime
            if timeFrame == 240:
                range = self._LevelMediator.calculateLevels("PD",candles,lookback=1)

                if len(range) > 0:
                    frameWorks.extend(range)

            if timeFrame == 1:
                if self.isInTime(time):
                    fvg = self._PDMediator.calculatePDArray("FVG", candles, lookback=3)
                    frameWorks.extend(fvg)

            return frameWorks

    def getEntry(self, candles: list, timeFrame: int):
        if candles and pds and len(candles) > 5 and timeFrame == 1:

                last_candle: Candle = candles[-1]
                prelast_candle: Candle = candles[-2]
                time = last_candle.isoTime

                if not self.isInTime(time):
                    return

                if len(levels) <= 0:
                    return

                fourHourCandle = levels[-1]

                directionSweep = ""

                for candle in candles:
                    if candle.close < fourHourCandle.level and fourHourCandle.direction == "Low":
                        directionSweep = "Bullish"
                    if candle.close < fourHourCandle.level and fourHourCandle.direction == "High":
                        directionSweep = "Bearish"


                oneMFvgs = [fvg for fvg in pds if fvg.name == "FVG" and fvg.status == "Inversed" and fvg.timeFrame == 1]

                currentInversed = []

                if len(oneMFvgs) > 0:
                    for fvg in oneMFvgs:
                        fvgRange = self._PDMediator.returnCandleRange(fvg.name,fvg)
                        if fvg.direction == "Bullish":
                            if prelast_candle.close > fvgRange.get('low') > last_candle.close:
                                currentInversed.append(fvg)
                        if fvg.direction == "Bearish":
                            if last_candle.close > fvgRange.get('high') > prelast_candle.close:
                                currentInversed.append(fvg)

    def getExit(self):
        pass
