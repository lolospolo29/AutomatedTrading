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

# Unicorn Entry with 4H PD Range Bias

class Unicorn(Strategy):
    def __init__(self, name: str):
        super().__init__(name,False,0)

        self._PDMediator = PDMediator()
        self._ConfirmationMediator = ConfirmationMediator()
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

    def returnExpectedTimeFrame(self) -> list:
        return self.expectedTimeFrames

    def isInTime(self,time) -> bool:
        if self._TimeWindow.IsInEntryWindow(time) or self._TimeWindow2.IsInEntryWindow(time):
            return True
        return False

    def analyzeData(self, candles: list, timeFrame: int) -> list:
            frameWorks = []
            if timeFrame == 240:
                ote = self._LevelMediator.calculateLevels("PD",candles,lookback=1)
                frameWorks.extend(ote)

            if timeFrame == 5:

                last_candle = candles[-1]
                time = last_candle.isoTime

                if self.isInTime(time):
                    breaker = self._PDMediator.calculatePDArray("BRK",candles)
                    if len(breaker) > 0:
                        frameWorks.extend(breaker)

                if self.isInTime(time):
                    fvg = self._PDMediator.calculatePDArray("FVG", candles, lookback=3)
                    frameWorks.extend(fvg)

            return frameWorks

    def getEntry(self, candles: list, timeFrame: int, pds: list[PDArray],
                 levels:list[Level], structures: list[Structure]):
        if candles and pds:

            last_candle: Candle = candles[-1]
            time = last_candle.isoTime

            if not self.isInTime(time):
                return

            if timeFrame == 5 and len(candles) > 10:
                breakers = [brk for brk in pds if brk.name == "Breaker"]
                fvgs = [brk for brk in pds if brk.name == "FVG"]

                for breaker in breakers:
                    breakerRange = self._PDMediator.returnCandleRange("BRK",breaker)
                    for fvg in fvgs:
                        fvgRange = self._PDMediator.returnCandleRange("FVG",fvg)

                        fvgLow = fvgRange.get('low')
                        fvgHigh = fvgRange.get('high')
                        breakerLow = breakerRange.get('low')
                        breakerHigh = breakerRange.get('high')

                        # Check if FVG and Breaker overlap
                        if fvgLow <= breakerHigh and fvgHigh >= breakerLow:
                            in_fvg_range = fvgLow <= last_candle.close <= fvgHigh

                            # Prüfen, ob der Schlusskurs in der Breaker-Range ist
                            in_breaker_range = breakerLow <= last_candle.close <= breakerHigh

                            # Prüfen, ob der Schlusskurs in beiden Ranges ist
                            if in_fvg_range and in_breaker_range:
                                if fvg.direction == "Bullish" and breaker.direction == "Bullish" :
                                    return "BUY"
                                if fvg.direction == "Bearish" and breaker.direction == "Bearish" :
                                    return "SELL"

    def getExit(self):
        pass
