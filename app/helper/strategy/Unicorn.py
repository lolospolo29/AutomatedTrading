from typing import Optional

from pydantic import Field

from app.helper.facade.StrategyFacade import StrategyFacade
from app.models.asset.Relation import Relation
from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


# Unicorn Entry with 4H PD Range Bias

class Unicorn(Strategy):
    model_config = {
        "arbitrary_types_allowed": True
    }
    strategy_facade: Optional['StrategyFacade'] = Field(default=None)

    def is_in_time(self, time) -> bool:
        if self._TimeWindow.is_in_entry_window(time) or self._TimeWindow2.is_in_entry_window(time):
            return True
        return False

    def _analyzeData(self, candles: list[Candle], timeFrame: int):
        if timeFrame == 240:
            ote = self._strategy_handler.LevelMediator.calculate_fibonacci("PD", candles, lookback=1)
            for level in ote:
                self._level_handler.add_level(level)

        if timeFrame == 5:

            last_candle = candles[-1]
            time = last_candle.iso_time

            if self.is_in_time(time):
                breaker = self._strategy_handler.PDMediator.calculate_pd_array("BRK", candles)
                for brk in breaker:
                    self._strategy_handler.pd_array_handler.add_pd_array(brk)

            if self.is_in_time(time):
                fvgs = self._strategy_handler.PDMediator.calculate_pd_array_with_lookback("FVG", candles, lookback=3)
                for fvg in fvgs:
                    self._strategy_handler.pd_array_handler.add_pd_array(fvg)

        self._strategy_handler.pd_array_handler.remove_pd_array(candles,timeFrame)
        self._strategy_handler.level_handler.remove_level(candles,timeFrame)

    def get_entry(self, candles: list[Candle], timeFrame: int, relation:Relation, asset_class:str) ->StrategyResult:
        self._analyzeData(candles, timeFrame)
        pds = self._strategy_handler.pd_array_handler.return_pd_arrays()
        if candles and pds and timeFrame == 5:

            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            if not self.is_in_time(time):
                return StrategyResult()

            if timeFrame == 5 and len(candles) > 10:
                breakers: list[PDArray] = [brk for brk in pds if brk.name == "Breaker"]
                fvgs: list[PDArray] = [brk for brk in pds if brk.name == "FVG"]

                for breaker in breakers:
                    breakerLow,breakerHigh = self._strategy_handler.PDMediator.return_candle_range("BRK", breaker)
                    for fvg in fvgs:
                        fvgLow,fvgHigh = self._strategy_handler.PDMediator.return_candle_range("FVG", fvg)

                        # Check if FVG and Breaker overlap
                        if fvgLow <= breakerHigh and fvgHigh >= breakerLow:
                            in_fvg_range = fvgLow <= last_candle.close <= fvgHigh

                            # Prüfen, ob der Schlusskurs in der Breaker-Range ist
                            in_breaker_range = breakerLow <= last_candle.close <= breakerHigh

                            # Prüfen, ob der Schlusskurs in beiden Ranges ist
                            if in_fvg_range and in_breaker_range:
                                if fvg.direction == "Bullish" and breaker.direction == "Bullish":
                                    return StrategyResult()

                                if fvg.direction == "Bearish" and breaker.direction == "Bearish":
                                    return StrategyResult()
        else:
            return StrategyResult()


    def get_exit(self, candles: list, timeFrame: int, trade:Trade, relation:Relation)->StrategyResult:
        pass
