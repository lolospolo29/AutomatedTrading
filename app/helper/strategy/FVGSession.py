from typing import Optional

from pydantic import Field

from app.helper.facade.StrategyFacade import StrategyFacade
from app.models.asset.Candle import Candle
from app.models.asset.Relation import Relation
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


# FVG CRT 4H
class FVGSession(Strategy):
    model_config = {
        "arbitrary_types_allowed": True
    }
    strategy_facade: Optional['StrategyFacade'] = Field(default=None)


    def is_in_time(self, time) -> bool:
        for time_window in self.time_windows:
            if time_window.is_in_entry_window(time):
                return True

    def _analyzeData(self, candles: list[Candle], timeFrame: int):
            last_candle = candles[-1]
            time = last_candle.iso_time
            if timeFrame == 240:
                range = self.strategy_facade.LevelMediator.calculate_fibonacci("PD", candles, lookback=1)
                for level in range:
                    self.strategy_facade.level_handler.add_level(level)


            if timeFrame == 1:
                if self.is_in_time(time):
                    fvgs = self.strategy_facade.PDMediator.calculate_pd_array_with_lookback("FVG", candles, lookback=3)
                    for fvg in fvgs:
                        self.strategy_facade.pd_array_handler.add_pd_array(fvg)
            self.strategy_facade.level_handler.remove_level(candles, timeFrame)
            self.strategy_facade.pd_array_handler.remove_pd_array(candles, timeFrame)


    def get_entry(self, candles: list[Candle], timeFrame: int, relation:Relation, asset_class:str)->StrategyResult:
        self._analyzeData(candles, timeFrame)
        pds = self.strategy_facade.pd_array_handler.detect_swing()
        levels = self.strategy_facade.level_handler.return_levels()
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
                    if candle.close < fourHourCandle.level and fourHourCandle._direction == "Low":
                        directionSweep = "Bullish"
                    if candle.close < fourHourCandle.level and fourHourCandle._direction == "High":
                        directionSweep = "Bearish"


                one_m_fvgs = [fvg for fvg in pds if fvg.name == "FVG" and fvg.timeframe == 1]

                current_inversed = []

                if len(one_m_fvgs) > 0:
                    for fvg in one_m_fvgs:
                        fvg_low,fvg_high = self.strategy_facade.PDMediator.return_candle_range(fvg.name, fvg)
                        if fvg._direction == "Bullish" and directionSweep == "Bearish":
                            if prelast_candle.close > fvg_low > last_candle.close:
                                current_inversed.append(fvg)
                        if fvg._direction == "Bearish" and directionSweep == "Bullish":
                            if last_candle.close > fvg_high > prelast_candle.close:
                                current_inversed.append(fvg)
                if len(current_inversed) > 0:
                    return StrategyResult()
        else:
            return StrategyResult()

    def get_exit(self, candles: list[Candle], timeFrame: int, trade: Trade, relation:Relation) -> StrategyResult:
        pass
