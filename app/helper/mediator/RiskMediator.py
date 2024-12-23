from typing import Tuple, Any

from app.models.asset.Candle import Candle
from app.models.riskCalculations.RiskModeEnum import RiskMode
from app.models.riskCalculations.entry.orderWeightage.OrderWeightage import OrderWeightage
from app.models.riskCalculations.entry.ratio.Models.ProfitStopEntry import ProfitStopEntry
from app.models.riskCalculations.entry.ratio.Modes.FixedRatio import FixedRatio
from app.models.riskCalculations.entry.ratio.Modes.RangeRatio import RangeRatio
from app.models.riskCalculations.entry.strategicStop.EndOfmbalance import EndOfImbalance
from app.models.riskCalculations.entry.strategicStop.OBStop import OBStop
from app.models.riskCalculations.entry.strategicStop.OBStopEnum import OrderBlockStop
from app.models.riskCalculations.entry.strategicStop.Swing import SwingStop
from app.models.riskCalculations.entry.technicalEntry.CE import CE
from app.models.riskCalculations.entry.technicalEntry.Drill import DrillEntry
from app.models.riskCalculations.entry.technicalEntry.Fill import FillEntry
from app.models.riskCalculations.exit.invalidation.InvalidationClose import InvalidationClose
from app.models.riskCalculations.exit.invalidation.InvalidationSteady import InvalidationSteady
from app.models.riskCalculations.exit.technicalStop.BreakEven import BreakEven
from app.models.riskCalculations.exit.technicalStop.TrailingStop import TrailingStop
from app.models.trade.OrderDirectionEnum import OrderDirection


class RiskMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RiskMediator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):  # Prevent re-initialization
            self._orderWeightage = OrderWeightage()
            self._fixedRatio = FixedRatio()
            self._rangeRatio = RangeRatio()
            self._swingStop = SwingStop()
            self._obStop = OBStop()
            self._endOfImbalance = EndOfImbalance()
            self._ce = CE()
            self._drill = DrillEntry()
            self._fill = FillEntry()
            self._invalidationClose = InvalidationClose()
            self._invalidationSteady = InvalidationSteady()
            self._be = BreakEven()
            self._trailingStop = TrailingStop()
            self._initialized: bool = True  # Mark as initialized

    def setOrderWeightagePercent(self, entries:list[ProfitStopEntry], mode: RiskMode) -> list[ProfitStopEntry]:
        return self._orderWeightage.setPercentagesBasedOnMode(entries, mode)

    # region  Entry Single Fixed Ratio Input
    def calculateFixedRatioStop(self,entry: float,profit: float,ratio: float,direction: OrderDirection)->Tuple[Any,bool]:
        return self._fixedRatio.calculateFixedRatioStop(entry, profit, ratio, direction)

    def calculateFixedProfit(self,entry: float,stop: float,ratio: float,direction: OrderDirection)->Tuple[Any,bool]:
        return self._fixedRatio.calculateFixedProfit(entry, stop, ratio, direction)

    def calculateFixedEntry(self, stop: float, profit: float, ratio: float, direction: OrderDirection)->Tuple[Any,bool]:
        return self._fixedRatio.calculateFixedEntry(stop, profit, ratio, direction)
    # endregion

    # region Entry List Fixed Ratio Input
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

    # region Entry Single Range Ratio Input
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

    # region Entry List Range Ratio Input
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

    # region Entry strategy Stop
    def getSwingStop(self,candle: Candle) -> float:
        return self._swingStop.getStrategyStop(candle)

    def getOBStop(self,candle: Candle,mode: OrderBlockStop) -> float:
        return self._obStop.getStrategyStop(candle, mode)

    def getImbalanceStop(self,candle: Candle) -> float:
        return self._endOfImbalance.getStrategyStop(candle)
    # endregion

    # region Entry Type
    def getCEEntry(self,candle: Candle) -> float:
        return self._ce.getEntry(candle)

    def getDrillEntry(self,candle: Candle) -> float:
        return self._drill.getEntry(candle)

    def getFillEntry(self,candle: Candle) -> float:
        return self._fill.getEntry(candle)
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

    #   Implement Profit Stop Analyzer

