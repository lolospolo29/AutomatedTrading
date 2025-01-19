from typing import Tuple, Any

from app.helper.calculator.ProfitStopAnalyzer import ProfitStopAnalyzer
from app.models.asset.Candle import Candle
from app.models.calculators.RiskModeEnum import RiskMode
from app.helper.calculator.PDRiskCalculator import PDRiskCalculator
from app.models.calculators.entry.orderWeightage.OrderWeightage import OrderWeightage
from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.entry.ratio.BaseRatio import BaseRatio
from app.models.calculators.entry.ratio.FixedRatio import FixedRatio
from app.models.calculators.entry.ratio.RangeRatio import RangeRatio
from app.models.calculators.exit.invalidation.InvalidationClose import InvalidationClose
from app.models.calculators.exit.invalidation.InvalidationSteady import InvalidationSteady
from app.models.calculators.exit.technicalStop.BreakEven import BreakEven
from app.models.calculators.exit.technicalStop.TrailingStop import TrailingStop
from app.models.trade.enums.OrderDirectionEnum import OrderDirectionEnum


class RiskCalculator:

    # region Initializing
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RiskCalculator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prevent re-initialization
            self._order_weightage = OrderWeightage()
            self._base_ratio = BaseRatio()
            self._fixed_ratio = FixedRatio()
            self._range_ratio = RangeRatio()
            self._invalidation_close = InvalidationClose()
            self._invalidation_steady = InvalidationSteady()
            self._be = BreakEven()
            self._trailing_stop = TrailingStop()
            self.pd_risk_calculator = PDRiskCalculator()
            self.profit_stop_analyzer = ProfitStopAnalyzer()
            self._initialized: bool = True  # Mark as initialized
    # endregion

    # region Order Weightage

    def set_order_weightage_percent(self, entries:list[ProfitStopEntry], mode: RiskMode) -> list[ProfitStopEntry]:
        return self._order_weightage.set_percentages_based_on_mode(entries, mode)


    # endregion

    # region Single Base Ratio Input
    def calculate_base_profit(self, entry:float, stop: float, ratio: float) -> float:
        return self._base_ratio.calculate_profit(entry, stop, ratio)

    def calculate_base_stop(self, entry:float, profit: float, ratio: float) -> float:
        return self._base_ratio.calculate_stop(entry, profit, ratio)

    def calculate_base_entry(self, stop:float, profit:float, ratio:float) -> float:
        return self._base_ratio.calculate_entry(stop, profit, ratio)
    # endregion

    # region  Single Fixed Ratio Input

    def calculate_fixed_profit(self, entry: float, stop: float, ratio: float, direction: OrderDirectionEnum)->Tuple[Any,bool]:
        return self._fixed_ratio.calculate_fixed_profit(entry, stop, ratio, direction)

    def calculate_fixed_ratio_stop(self, entry: float, profit: float, ratio: float, direction: OrderDirectionEnum)->Tuple[Any,bool]:
        return self._fixed_ratio.calculate_fixed_ratio_stop(entry, profit, ratio, direction)

    def calculate_fixed_entry(self, stop: float, profit: float, ratio: float, direction: OrderDirectionEnum)->Tuple[Any,bool]:
        return self._fixed_ratio.calculate_fixed_entry(stop, profit, ratio, direction)
    # endregion

    # region List Fixed Ratio Input
    def calculate_profits_fixed(self, entries: list[float], stops: list[float], ratio: float,
                                direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        return self._fixed_ratio.calculate_profits(entries, stops, ratio, direction)

    def calculate_stops_fixed(self, entries: list[float], profits: list[float], ratio: float,
                              direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        return self._fixed_ratio.calculate_stops(entries, profits, ratio, direction)

    def calculate_entries_fixed(self, stops: list[float], profits: list[float], ratio: float,
                                direction: OrderDirectionEnum)-> list[ProfitStopEntry]:
        return self._fixed_ratio.calculate_entries(stops, profits, ratio, direction)
    # endregion

    # region Invalidation Exit
    def check_invalidation_close(self, stop: float, candle: Candle, direction: OrderDirectionEnum) -> bool:
        return self._invalidation_close.check_invalidation(stop, candle, direction)

    def check_invalidation(self, stop: float, candle: Candle, direction: OrderDirectionEnum) ->bool:
        return self._invalidation_steady.check_invalidation(stop, candle, direction)
    # endregion

    # region Move Stop Exit
    def is_price_in_break_even_range(self, currentPrice:float, entry: float, takeProfit: float) -> bool:
        return self._be.IsPriceInBreakEvenRange(currentPrice, entry, takeProfit)

    def return_fibonnaci_trailing(self, currentPrice: float, stop: float, entry: float) -> float:
        return self._trailing_stop.returnFibonnaciTrailing(currentPrice, stop, entry)
    # endregion

    # region Single Range Ratio Input
    def calculate_range_profits(self, entry: float, stop: float, rangeRatio: list[float],
                                direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        return self._range_ratio.calculate_range_profits(entry, stop, rangeRatio, direction)

    def calculate_range_stops(self, entry: float, profit: float, rangeRatio: list[float]
                              , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        return self._range_ratio.calculate_range_stops(entry, profit, rangeRatio, direction)

    def calculate_range_entries(self, stop: float, profit: float, rangeRatio: list[float]
                                , direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        return self._range_ratio.calculate_range_entries(stop, profit, rangeRatio, direction)
    # endregion

    # region List Range Ratio Input
    def calculate_profits_range(self, entries: list[float], stops: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        return self._range_ratio.calculate_profits(entries, stops, rangeRatio, direction)

    def calculate_stops_range(self, entries: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        return self._range_ratio.calculate_stops(entries, profits, rangeRatio, direction)

    def calculate_entries_range(self, stops: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirectionEnum) -> list[ProfitStopEntry]:
        return self._range_ratio.calculate_entries(stops, profits, rangeRatio, direction)
    # endregion