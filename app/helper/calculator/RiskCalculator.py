from typing import Tuple, Any

from app.models.calculators.ProfitStopAnalyzer import ProfitStopAnalyzer
from app.models.asset.Candle import Candle
from app.models.calculators.frameworks.PDArray import PDArray
from app.models.calculators.RiskModeEnum import RiskMode
from app.models.calculators.entry.PDRiskCalculator import PDRiskCalculator
from app.models.calculators.entry.orderWeightage.OrderWeightage import OrderWeightage
from app.models.calculators.ProfitStopEntry import ProfitStopEntry
from app.models.calculators.entry.ratio.BaseRatio import BaseRatio
from app.models.calculators.entry.ratio.FixedRatio import FixedRatio
from app.models.calculators.entry.ratio.RangeRatio import RangeRatio
from app.models.calculators.exit.invalidation.InvalidationClose import InvalidationClose
from app.models.calculators.exit.invalidation.InvalidationSteady import InvalidationSteady
from app.models.calculators.exit.technicalStop.BreakEven import BreakEven
from app.models.calculators.exit.technicalStop.TrailingStop import TrailingStop
from app.models.trade.enums.OrderDirectionEnum import OrderDirection


class RiskCalculator:

    # region Initializing
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RiskCalculator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prevent re-initialization
            self._orderWeightage = OrderWeightage()
            self._baseRatio = BaseRatio()
            self._fixedRatio = FixedRatio()
            self._rangeRatio = RangeRatio()
            self._invalidationClose = InvalidationClose()
            self._invalidationSteady = InvalidationSteady()
            self._be = BreakEven()
            self._trailingStop = TrailingStop()
            self._pdRiskCalculator = PDRiskCalculator()
            self.profitStopAnalyzer = ProfitStopAnalyzer()
            self._initialized: bool = True  # Mark as initialized
    # endregion

    # region Order Weightage

    def setOrderWeightagePercent(self, entries:list[ProfitStopEntry], mode: RiskMode) -> list[ProfitStopEntry]:
        return self._orderWeightage.setPercentagesBasedOnMode(entries, mode)

    # endregion

    # region Calculate Stops PD's
    def calculatePDStops(self, pdArrays: list[PDArray], orderDirection: OrderDirection) -> list[float]:
        return self._pdRiskCalculator.calculateAllStops(pdArrays, orderDirection)

    def calculatePDStopsSpecific(self,pdArrays: list[PDArray], orderDirection: OrderDirection,riskMode: RiskMode) -> list[float]:
        return self._pdRiskCalculator.calculateStopsSpecific(pdArrays, orderDirection, riskMode)
    # endregion

    # region Calculate Entries PD's
    def calculatePDEntries(self, pdArrays: list[PDArray], orderDirection: OrderDirection) -> list[float]:
        return self._pdRiskCalculator.calculateAllEntries(pdArrays, orderDirection)
    def calculatePDEntriesSpecific(self,pdArrays: list[PDArray], orderDirection: OrderDirection,riskMode: RiskMode) -> list[float]:
        return self._pdRiskCalculator.calculateEntriesSpecific(pdArrays, orderDirection, riskMode)
    # endregion

    # region Single Base Ratio Input
    def calculateBaseProfit(self,entry:float, stop: float, ratio: float) -> float:
        return self._baseRatio.calculateProfit(entry, stop, ratio)

    def calculateBaseStop(self,entry:float, profit: float, ratio: float) -> float:
        return self._baseRatio.calculateStop(entry, profit, ratio)

    def calculateBaseEntry(self,stop:float, profit:float, ratio:float) -> float:
        return self._baseRatio.calculateEntry(stop, profit, ratio)
    # endregion

    # region  Single Fixed Ratio Input

    def calculateFixedProfit(self,entry: float,stop: float,ratio: float,direction: OrderDirection)->Tuple[Any,bool]:
        return self._fixedRatio.calculateFixedProfit(entry, stop, ratio, direction)

    def calculateFixedRatioStop(self,entry: float,profit: float,ratio: float,direction: OrderDirection)->Tuple[Any,bool]:
        return self._fixedRatio.calculateFixedRatioStop(entry, profit, ratio, direction)

    def calculateFixedEntry(self, stop: float, profit: float, ratio: float, direction: OrderDirection)->Tuple[Any,bool]:
        return self._fixedRatio.calculateFixedEntry(stop, profit, ratio, direction)
    # endregion

    # region List Fixed Ratio Input
    def calculateProfitsFixed(self, entries: list[float], stops: list[float], ratio: float,
                         direction: OrderDirection)-> list[ProfitStopEntry]:
        return self._fixedRatio.calculateProfits(entries, stops, ratio, direction)

    def calculateStopsFixed(self, entries: list[float], profits: list[float], ratio: float,
                       direction: OrderDirection)-> list[ProfitStopEntry]:
        return self._fixedRatio.calculateStops(entries, profits, ratio, direction)

    def calculateEntriesFixed(self, stops: list[float], profits: list[float], ratio: float,
                         direction: OrderDirection)-> list[ProfitStopEntry]:
        return self._fixedRatio.calculateEntries(stops, profits, ratio, direction)
    # endregion

    # region Single Range Ratio Input
    def calculateRangeProfits(self, entry: float, stop: float, rangeRatio: list[float],
                              direction: OrderDirection) -> list[ProfitStopEntry]:
        return self._rangeRatio.calculateRangeProfits(entry, stop, rangeRatio, direction)

    def calculateRangeStops(self, entry: float, profit: float, rangeRatio: list[float]
                            , direction: OrderDirection) -> list[ProfitStopEntry]:
        return self._rangeRatio.calculateRangeStops(entry, profit, rangeRatio, direction)

    def calculateRangeEntries(self, stop: float, profit: float, rangeRatio: list[float]
                              , direction: OrderDirection) -> list[ProfitStopEntry]:
        return self._rangeRatio.calculateRangeEntries(stop, profit, rangeRatio, direction)
    # endregion

    # region List Range Ratio Input
    def calculateProfitsRange(self, entries: list[float], stops: list[float], rangeRatio:
    list[int], direction: OrderDirection) -> list[ProfitStopEntry]:
        return self._rangeRatio.calculateProfits(entries, stops, rangeRatio, direction)

    def calculateStopsRange(self, entries: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirection) -> list[ProfitStopEntry]:
        return self._rangeRatio.calculateStops(entries, profits, rangeRatio, direction)

    def calculateEntriesRange(self, stops: list[float], profits: list[float], rangeRatio:
    list[int], direction: OrderDirection) -> list[ProfitStopEntry]:
        return self._rangeRatio.calculateEntries(stops, profits, rangeRatio, direction)
    # endregion

    # region Invalidation Exit
    def checkInvalidationClose(self,stop: float, candle: Candle, direction: OrderDirection) -> bool:
        return self._invalidationClose.checkInvalidation(stop, candle, direction)

    def checkInvalidation(self,stop: float, candle: Candle, direction: OrderDirection) ->bool:
        return self._invalidationSteady.checkInvalidation(stop, candle, direction)
    # endregion

    # region Move Stop Exit
    def IsPriceInBreakEvenRange(self, currentPrice:float, entry: float, takeProfit: float) -> bool:
        return self._be.IsPriceInBreakEvenRange(currentPrice, entry, takeProfit)

    def returnFibonnaciTrailing(self,currentPrice: float, stop: float, entry: float) -> float:
        return self._trailingStop.returnFibonnaciTrailing(currentPrice, stop, entry)
    # endregion

    # todo Implement Profit Stop Analyzer

