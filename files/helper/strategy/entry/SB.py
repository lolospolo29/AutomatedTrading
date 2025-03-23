from files.models.asset.Candle import Candle
from files.models.asset.Relation import Relation
from files.models.frameworks.PDArray import PDArray
from files.models.strategy import EntryInput
from files.models.strategy.EntryStrategy import EntryStrategy
from files.models.strategy.Result import StrategyResult


# Unicorn Entry with 4H PD Range Bias

class LondonSB(EntryStrategy):

    @property
    def name(self) -> str:
        pass

    def get_entry(self, entryInput: EntryInput) -> StrategyResult:
        pass

    def is_in_time(self, time) -> bool:
        pass

    def return_expected_time_frame(self) -> list:
        return self.expectedTimeFrames

    def _analyzeData(self, candles: list[Candle], timeFrame: int):

        if timeFrame == 240:
            pds = self.strategy_facade.LevelMediator.calculate_fibonacci("PD", candles, lookback=1)
            for pd in pds:
                self.strategy_facade.level_handler.add_level(pd)

        if timeFrame == 5:
            structures = self.strategy_facade.StructureMediator.calculate_confirmation("BOS", candles)
            for structure in structures:
                self.strategy_facade.structure_handler.add_structure(structure)

        if timeFrame == 1:

            last_candle = candles[-1]
            time = last_candle.iso_time

            if self.is_in_time(time):
                fvgs = self.strategy_facade.PDMediator.calculate_pd_array_with_lookback("FVG", candles, lookback=3)
                for fvg in fvgs:
                    self.strategy_facade.pd_array_handler.add_pd_array(fvg)

        self.strategy_facade.pd_array_handler.remove_pd_array(candles, timeFrame)
        self.strategy_facade.structure_handler.remove_structure(candles, timeFrame)

    def entry(self, candles: list[Candle], timeFrame: int, relation:Relation, asset_class:str) ->StrategyResult:
        self._analyzeData(candles, timeFrame)
        pds = self.strategy_facade.pd_array_handler._detect_swing()
        structures = self.strategy_facade.structure_handler.return_structure()
        levels = self.strategy_facade.level_handler.return_levels()
        if candles and pds and structures and levels and timeFrame == 1:

            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            last_structure = structures[-1]

            if not self.is_in_time(time):
                return StrategyResult()

            fvgs: list[PDArray] = [brk for brk in pds if brk._name == "FVG"]

            for fvg in fvgs:
                fvgLow, fvgHigh = self.strategy_facade.PDMediator.return_candle_range("FVG", fvg)
                if fvgLow <= last_candle.close <= fvgHigh:
                    if last_structure._direction == "Bullish":
                        return StrategyResult()
                    if last_structure._direction == "Bearish":
                        return StrategyResult()
        else:
            return StrategyResult()