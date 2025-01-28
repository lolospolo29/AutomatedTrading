from app.helper.handler.LevelHandler import LevelHandler
from app.helper.handler.PDArrayHandler import PDArrayHandler
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
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


# FVG CRT 4H
class FVGSession(Strategy):
    def __init__(self):
        name:str = "FVG"

        self._PDMediator = PDMediator()
        self._ConfirmationMediator = StructureMediator()
        self._LevelMediator : LevelMediator= LevelMediator()

        self._TimeWindow = LondonOpen()
        self._TimeWindow2 = NYOpen()

        self._level_handler = LevelHandler()
        self._pd_array_handler = PDArrayHandler()

        self.expectedTimeFrames = []


        timeFrame = ExpectedTimeFrame(1,90)
        timeFrame2 = ExpectedTimeFrame(5,90)
        timeFrame3 = ExpectedTimeFrame(15,90)
        timeFrame4 = ExpectedTimeFrame(240,1)

        self.expectedTimeFrames.append(timeFrame)
        self.expectedTimeFrames.append(timeFrame2)
        self.expectedTimeFrames.append(timeFrame3)
        self.expectedTimeFrames.append(timeFrame4)
        super().__init__(name,self.expectedTimeFrames)


    def is_in_time(self, time) -> bool:
        if self._TimeWindow.is_in_entry_window(time) or self._TimeWindow2.is_in_entry_window(time):
            return True
        return False

    def _analyzeData(self, candles: list, timeFrame: int):
            last_candle = candles[-1]
            time = last_candle.iso_time
            if timeFrame == 240:
                range = self._LevelMediator.calculate_fibonacci("PD", candles, lookback=1)
                for level in range:
                    self._level_handler.add_level(level)


            if timeFrame == 1:
                if self.is_in_time(time):
                    fvgs = self._PDMediator.calculate_pd_array("FVG", candles, lookback=3)
                    for fvg in fvgs:
                        self._pd_array_handler.add_pd_array(fvg)
            self._pd_array_handler.remove_pd_array(candles,timeFrame)
            self._level_handler.remove_level(candles,timeFrame)


    def get_entry(self, candles: list, timeFrame: int)->StrategyResult:
        self._analyzeData(candles, timeFrame)
        pds = self._pd_array_handler.return_pd_arrays()
        levels = self._level_handler.return_levels()
        if candles and pds and len(candles) > 5 and timeFrame == 1:

                last_candle: Candle = candles[-1]
                prelast_candle: Candle = candles[-2]
                time = last_candle.iso_time

                if not self.is_in_time(time):
                    return StrategyResult()

                if len(levels) <= 0:
                    return StrategyResult()

                fourHourCandle = levels[-1]

                directionSweep = ""

                for candle in candles:
                    if candle.close < fourHourCandle.level and fourHourCandle.direction == "Low":
                        directionSweep = "Bullish"
                    if candle.close < fourHourCandle.level and fourHourCandle.direction == "High":
                        directionSweep = "Bearish"


                oneMFvgs = [fvg for fvg in pds if fvg.name == "FVG" and fvg.timeframe == 1]

                currentInversed = []

                if len(oneMFvgs) > 0:
                    for fvg in oneMFvgs:
                        fvg_low,fvg_high = self._PDMediator.return_candle_range(fvg.name, fvg)
                        if fvg.direction == "Bullish" and directionSweep == "Bearish":
                            if prelast_candle.close > fvg_low > last_candle.close:
                                currentInversed.append(fvg)
                        if fvg.direction == "Bearish" and directionSweep == "Bullish":
                            if last_candle.close > fvg_high > prelast_candle.close:
                                currentInversed.append(fvg)
                if len(currentInversed) > 0:
                    return StrategyResult()

    def get_exit(self, candles: list[Candle], timeFrame: int, trade: Trade) -> StrategyResult:
        pass
