from app.helper.facade.StrategyFacade import StrategyFacade
from app.models.asset.Candle import Candle
from app.models.asset.Relation import Relation
from app.models.frameworks.PDArray import PDArray
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


# Unicorn Entry with 4H PD Range Bias

class LondonSB(Strategy):
    _strategy_facade:StrategyFacade = StrategyFacade()

    def return_expected_time_frame(self) -> list:
        return self.expectedTimeFrames

    def is_in_time(self, time) -> bool:
        if self._silver_bullet_london.is_in_entry_window(time):
            return True
        return False

    def _analyzeData(self, candles: list[Candle], timeFrame: int):

        if timeFrame == 240:
            pds = self._strategy_facade.LevelMediator.calculate_fibonacci("PD", candles, lookback=1)
            for pd in pds:
                self._strategy_facade.level_handler.add_level(pd)

        if timeFrame == 5:
            structures = self._strategy_facade.StructureMediator.calculate_confirmation("BOS",candles)
            for structure in structures:
                self._strategy_facade.structure_handler.add_structure(structure)

        if timeFrame == 1:

            last_candle = candles[-1]
            time = last_candle.iso_time

            if self.is_in_time(time):
                fvgs = self._strategy_facade.PDMediator.calculate_pd_array_with_lookback("FVG", candles, lookback=3)
                for fvg in fvgs:
                    self._strategy_facade.pd_array_handler.add_pd_array(fvg)

        self._strategy_facade.pd_array_handler.remove_pd_array(candles,timeFrame)
        self._strategy_facade.structure_handler.remove_structure(candles,timeFrame)

    def get_entry(self, candles: list[Candle], timeFrame: int, relation:Relation, asset_class:str) ->StrategyResult:
        self._analyzeData(candles, timeFrame)
        pds = self._strategy_facade.pd_array_handler.return_pd_arrays()
        structures = self._strategy_facade.structure_handler.return_structure()
        levels = self._strategy_facade.level_handler.return_levels()
        if candles and pds and structures and levels and timeFrame == 1:

            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            last_structure = structures[-1]

            if not self.is_in_time(time):
                return StrategyResult()

            fvgs: list[PDArray] = [brk for brk in pds if brk.name == "FVG"]

            for fvg in fvgs:
                fvgLow, fvgHigh = self._strategy_facade.PDMediator.return_candle_range("FVG", fvg)
                if fvgLow <= last_candle.close <= fvgHigh:
                    if last_structure.direction == "Bullish":
                        return StrategyResult()
                    if last_structure.direction == "Bearish":
                        return StrategyResult()
        else:
            return StrategyResult()

    def get_exit(self, candles: list, timeFrame: int, trade:Trade, relation:Relation)->StrategyResult:
        pass
