from app.helper.facade.StrategyFacade import StrategyFacade
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.Structure import Structure
from app.models.calculators.frameworks.time.Asia import Asia
from app.models.calculators.frameworks.time.London import LondonOpen
from app.models.calculators.frameworks.time.NYOpen import NYOpen
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


# FVG CRT 4H
class OTEFourH(Strategy):
    def __init__(self):
        name:str = "OTEFourH"

        self._strategy_facade = StrategyFacade()

        self._TimeWindow = LondonOpen()
        self._TimeWindow2 = NYOpen()
        self._TimeWindow3 = Asia()

        self.expectedTimeFrames = []

        timeFrame3 = ExpectedTimeFrame(15,90)
        timeFrame4 = ExpectedTimeFrame(240,90)

        self.expectedTimeFrames.append(timeFrame3)
        self.expectedTimeFrames.append(timeFrame4)
        super().__init__(name,self.expectedTimeFrames)


    def is_in_time(self, time) -> bool:
        return True

    def _analyzeData(self, candles: list[Candle], timeFrame: int):
            if timeFrame == 240 and len(candles) > 20 :
                range = self._strategy_facade.LevelMediator.calculate_fibonacci("OTE", candles, lookback=20)
                for level in range:
                    level.timeframe = 240
                    self._strategy_facade.level_handler.add_level(level)
                fvgs = self._strategy_facade.PDMediator.calculate_pd_array("FVG", candles)
                for fvg in fvgs:
                        fvg.timeframe = 240
                        self._strategy_facade.pd_array_handler.add_pd_array(fvg)
                structures = self._strategy_facade.StructureMediator.calculate_confirmation("BOS",candles)
                for structure in structures:
                    structure.timeframe = 240
                    self._strategy_facade.structure_handler.add_structure(structure)

                self._strategy_facade.level_handler.remove_level(candles, timeFrame)
                self._strategy_facade.pd_array_handler.remove_pd_array(candles, timeFrame)
                self._strategy_facade.structure_handler.remove_structure(candles, timeFrame)


    def get_entry(self, candles: list[Candle], timeFrame: int)->StrategyResult:
        self._analyzeData(candles, timeFrame)
        pds = self._strategy_facade.pd_array_handler.return_pd_arrays()
        levels = self._strategy_facade.level_handler.return_levels()
        structures = self._strategy_facade.structure_handler.return_structure()
        if candles and pds and timeFrame == 240 and len(levels) > 3 and structures and len(candles) > 20:
            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            latest_structure:Structure = structures[-1]

            last_four_levels = levels[-4:]

            fvgs = [fvg for fvg in pds if fvg.name == "FVG" and fvg.timeframe == 240]

            min_level = min(last_four_levels, key=lambda x: x.level and x.direction == latest_structure.direction)
            max_level = max(last_four_levels, key=lambda x: x.level and x.direction == latest_structure.direction)

            for fvg in fvgs:
                fvg_low,fvg_high = self._strategy_facade.PDMediator.return_candle_range(fvg.name, fvg)
                if fvg.direction == latest_structure.direction:
                    if fvg_high >= min_level.level and fvg_low <= max_level.level:
                        return StrategyResult()

    def get_exit(self, candles: list[Candle], timeFrame: int, trade: Trade) -> StrategyResult:
        pass
