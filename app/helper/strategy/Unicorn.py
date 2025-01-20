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
from app.models.trade.Order import Order
from app.helper.calculator.RiskCalculator import RiskCalculator

# Unicorn Entry with 4H PD Range Bias

class Unicorn(Strategy):
    def __init__(self):
        name:str = "Unicorn"
        super().__init__(name,False)

        self._PDMediator = PDMediator()
        self._ConfirmationMediator = StructureMediator()
        self._LevelMediator : LevelMediator= LevelMediator()
        self._RiskMediator : RiskCalculator= RiskCalculator()

        self._TimeWindow = LondonOpen()
        self._TimeWindow2 = NYOpen()
        #todo


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
        if self._TimeWindow.is_in_entry_window(time) or self._TimeWindow2.is_in_entry_window(time):
            return True
        return False

    def analyzeData(self, candles: list, timeFrame: int) -> list:
            frameWorks = []
            if timeFrame == 240:
                ote = self._LevelMediator.calculate_fibonacci("PD", candles, lookback=1)
                frameWorks.extend(ote)

            if timeFrame == 5:

                last_candle = candles[-1]
                time = last_candle.iso_time

                if self.isInTime(time):
                    breaker = self._PDMediator.calculate_pd_array("BRK", candles)
                    if len(breaker) > 0:
                        frameWorks.extend(breaker)

                if self.isInTime(time):
                    fvg = self._PDMediator.calculate_pd_array_with_lookback("FVG", candles, lookback=3)
                    frameWorks.extend(fvg)

            return frameWorks

    def getEntry(self, candles: list, timeFrame: int, pds: list[PDArray],
                 levels:list[Level], structures: list[Structure]) ->list[Order]:
        if candles and pds:

            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            if not self.isInTime(time):
                return []

            if timeFrame == 5 and len(candles) > 10:
                breakers:list[PDArray] = [brk for brk in pds if brk.name == "Breaker"]
                fvgs:list[PDArray] = [brk for brk in pds if brk.name == "FVG"]

                for breaker in breakers:
                    breakerRange = self._PDMediator.return_candle_range("BRK", breaker)
                    for fvg in fvgs:
                        fvgRange = self._PDMediator.return_candle_range("FVG", fvg)
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
                                    pass

                                if fvg.direction == "Bearish" and breaker.direction == "Bearish" :
                                    return "SELL"

    def returnOrder(self, lastCandle:Candle,candles: list, timeFrame: int,direction: str) -> Order:

        middleCandle = candles[0]

        pass


    def getExit(self):
        pass
