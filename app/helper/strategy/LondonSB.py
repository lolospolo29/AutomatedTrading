from app.helper.facade.StrategyFacade import StrategyFacade
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.frameworks.time.macro.silverBullet.SilverBulletLondon import SilverBulletLondon
from app.models.strategy.ExpectedTimeFrame import ExpectedTimeFrame
from app.models.strategy.Strategy import Strategy
from app.models.strategy.StrategyResult import StrategyResult
from app.models.trade.Trade import Trade


# Unicorn Entry with 4H PD Range Bias

class LondonSB(Strategy):
    def __init__(self):
        name: str = "LondonSB"

        self._strategy_facade = StrategyFacade()

        self._silver_bullet_london = SilverBulletLondon()

        self.expectedTimeFrames = []

        timeFrame = ExpectedTimeFrame(1, 90)
        timeFrame2 = ExpectedTimeFrame(5, 90)
        timeFrame4 = ExpectedTimeFrame(60, 1)

        self.expectedTimeFrames.append(timeFrame)
        self.expectedTimeFrames.append(timeFrame2)
        self.expectedTimeFrames.append(timeFrame4)

        super().__init__(name, self.expectedTimeFrames)

    def return_expected_time_frame(self) -> list:
        return self.expectedTimeFrames

    def is_in_time(self, time) -> bool:
        if self._silver_bullet_london.is_in_entry_window(time):
            return True
        return False

    def _analyzeData(self, candles: list, timeFrame: int):

        if timeFrame == 60:
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

    def get_entry(self, candles: list, timeFrame: int) ->StrategyResult:
        self._analyzeData(candles, timeFrame)
        pds = self._strategy_facade.pd_array_handler.return_pd_arrays()
        structures = self._strategy_facade.structure_handler.return_structure()
        if candles and pds and structures and timeFrame == 1:

            last_candle: Candle = candles[-1]
            time = last_candle.iso_time

            last_structure = structures[-1]

            if not self.is_in_time(time):
                return StrategyResult()

            if timeFrame == 5 and len(candles) > 10:
                fvgs: list[PDArray] = [brk for brk in pds if brk.name == "FVG"]
                pds: list[PDArray] = [pd for pd in pds if pd.name == "PD"]

                for fvg in fvgs:
                    fvgLow,fvgHigh = self._strategy_facade.PDMediator.return_candle_range("FVG", fvg)
                    if fvgLow <= last_candle.close <= fvgHigh:
                        if last_structure.direction == "Bullish":
                            return StrategyResult()


    def get_exit(self, candles: list, timeFrame: int, trade:Trade)->StrategyResult:
        pass
