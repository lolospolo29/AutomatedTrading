from typing import Optional

from pydantic import Field

from app.helper.facade.StrategyFacade import StrategyFacade
from app.models.asset.Relation import Relation
from app.models.asset.Candle import Candle
from app.models.frameworks.PDArray import PDArray
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


class NYMSS(Strategy):
    name:str =Field(default='FVGSession')
    model_config = {
        "arbitrary_types_allowed": True
    }
    strategy_facade: Optional['StrategyFacade'] = Field(default=None)
    def return_expected_time_frame(self) -> list:
        return self.expectedTimeFrames

    def is_in_time(self, time) -> bool:
        for time_window in self.time_windows:
            if time_window.is_in_entry_window(time):
                return True
        return False

    def _analyzeData(self, candles: list[Candle], timeFrame: int):
        if timeFrame == 60:
            fvgs = self._strategy_handler.PDMediator.calculate_pd_array("FVG", candles)
            for fvg in fvgs:
                fvg.timeframe = 60
                self._level_handler.add_level(fvg)

        if timeFrame == 5:

            last_candle = candles[-1]
            time = last_candle.iso_time

            if self.is_in_time(time):
                fvgs = self._strategy_handler.PDMediator.calculate_pd_array_with_lookback("FVG", candles, lookback=3)
                for fvg in fvgs:
                    self._strategy_handler.pd_array_handler.add_pd_array(fvg)

        self._strategy_handler.pd_array_handler.remove_pd_array(candles,timeFrame)

    def get_entry(self, candles: list[Candle], timeFrame: int, relation:Relation, asset_class:str) ->StrategyResult:
        self._analyzeData(candles, timeFrame)
        pds:list[PDArray] = self._strategy_handler.pd_array_handler.return_pd_arrays()
        if candles and pds and timeFrame == 5:

            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            if not self.is_in_time(time):
                return StrategyResult()

            fvgs_one_hour: list[PDArray] = [fvg for fvg in pds if fvg.name == "FVG" and fvg.timeframe == 60]
            fvgs_five_minute:list[PDArray] = [fvg for fvg in pds if fvg.name == "FVG" and fvg.timeframe == 5]

            for fvg1 in fvgs_one_hour:
                fvg_one_h_low, fvg_one_h_high = self._strategy_handler.PDMediator.return_candle_range("FVG", fvg1)
                for fvg5 in fvgs_five_minute:
                    fvg_five_min_low, fvg_five_min_high = self._strategy_handler.PDMediator.return_candle_range("FVG", fvg5)
                    if fvg1.direction == fvg5.direction:
                        if fvg_one_h_low <= fvg_five_min_low and fvg_one_h_high >= fvg_five_min_high:
                            if fvg1.direction == "Bullish":
                                return StrategyResult()
                            if fvg1.direction == "Bearish":
                                return StrategyResult()
        else:
            return StrategyResult()



    def get_exit(self, candles: list, timeFrame: int, trade:Trade, relation:Relation)->StrategyResult:
        pass
