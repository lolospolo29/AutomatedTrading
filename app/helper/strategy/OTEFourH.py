from typing import Optional

from pydantic import Field

from app.helper.facade.StrategyFacade import StrategyFacade
from app.models.asset.Relation import Relation
from app.models.asset.Candle import Candle
from app.models.frameworks.Structure import Structure
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


class OTEFourH(Strategy):
    """
    Implements a trading strategy called OTEFourH. This class is a specialization of the Strategy
    base class and is specifically tailored to operate on specific timeframes and market conditions.
    It incorporates time window functionality for different trading sessions (London, New York, Asia)
    alongside expected timeframes relevant for analysis and decision-making. The strategy leverages
    components such as level calculations, pattern detection, Fibonacci retracements, and confirmation
    structures to generate trading entries and exits.
    """
    model_config = {
        "arbitrary_types_allowed": True
    }
    strategy_facade: Optional['StrategyFacade'] = Field(default=None)

    def is_in_time(self, time) -> bool:
        return True

    def _analyzeData(self, candles: list[Candle], timeFrame: int):
            if timeFrame == 240 and len(candles) > 20 :
                range = self.strategy_facade.LevelMediator.calculate_fibonacci("OTE", candles, lookback=20)
                for level in range:
                    level.timeframe = 240
                    self.strategy_facade.level_handler.add_level(level)
                fvgs = self.strategy_facade.PDMediator.calculate_pd_array("FVG", candles)
                for fvg in fvgs:
                        fvg.timeframe = 240
                        self.strategy_facade.pd_array_handler.add_pd_array(fvg)
                structures = self.strategy_facade.StructureMediator.calculate_confirmation("BOS", candles)
                for structure in structures:
                    structure.timeframe = 240
                    self.strategy_facade.structure_handler.add_structure(structure)

                self.strategy_facade.level_handler.remove_level(candles, timeFrame)
                self.strategy_facade.pd_array_handler.remove_pd_array(candles, timeFrame)
                self.strategy_facade.structure_handler.remove_structure(candles, timeFrame)


    def get_entry(self, candles: list[Candle], timeFrame: int, relation:Relation, asset_class:str)->StrategyResult:
        self._analyzeData(candles, timeFrame)
        pds = self.strategy_facade.pd_array_handler.return_pd_arrays()
        levels = self.strategy_facade.level_handler.return_levels()
        structures = self.strategy_facade.structure_handler.return_structure()
        if candles and pds and timeFrame == 240 and len(levels) > 3 and structures and len(candles) > 20:
            latest_structure:Structure = structures[-1]

            last_four_levels = levels[-4:]

            fvgs = [fvg for fvg in pds if fvg.name == "FVG" and fvg.timeframe == 240]

            min_level = min(last_four_levels, key=lambda x: x.level and x.direction == latest_structure.direction)
            max_level = max(last_four_levels, key=lambda x: x.level and x.direction == latest_structure.direction)

            for fvg in fvgs:
                fvg_low,fvg_high = self.strategy_facade.PDMediator.return_candle_range(fvg.name, fvg)
                if fvg.direction == latest_structure.direction:
                    if fvg_high >= min_level.level and fvg_low <= max_level.level:
                        return StrategyResult()
        else:
            return StrategyResult()


    def get_exit(self, candles: list[Candle], timeFrame: int, trade: Trade, relation:Relation) -> StrategyResult:
        pass
