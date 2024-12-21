from typing import Tuple, Any

from Core.Main.Asset.SubModels.Candle import Candle
from Core.Main.Trade.OrderDirectionEnum import OrderDirection
from Core.Main.Trade.RiskFrameWorks.Entry.OrderWeightage.OrderWeightage import OrderWeightage
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Models.ProfitStopEntry import ProfitStopEntry
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Modes.FixedRatio import FixedRatio
from Core.Main.Trade.RiskFrameWorks.Entry.Ratio.Modes.RangeRatio import RangeRatio
from Core.Main.Trade.RiskFrameWorks.Entry.StrategicStop.EndOfmbalance import EndOfImbalance
from Core.Main.Trade.RiskFrameWorks.Entry.StrategicStop.OBStop import OBStop
from Core.Main.Trade.RiskFrameWorks.Entry.StrategicStop.OBStopEnum import OrderBlockStop
from Core.Main.Trade.RiskFrameWorks.Entry.StrategicStop.Swing import SwingStop
from Core.Main.Trade.RiskFrameWorks.Entry.TechnicalEntry.CE import CE
from Core.Main.Trade.RiskFrameWorks.Entry.TechnicalEntry.Drill import DrillEntry
from Core.Main.Trade.RiskFrameWorks.Entry.TechnicalEntry.Fill import FillEntry
from Core.Main.Trade.RiskFrameWorks.Exit.Invalidation.InvalidationClose import InvalidationClose
from Core.Main.Trade.RiskFrameWorks.Exit.Invalidation.InvalidationSteady import InvalidationSteady
from Core.Main.Trade.RiskFrameWorks.Exit.TechnicalStop.BreakEven import BreakEven
from Core.Main.Trade.RiskFrameWorks.Exit.TechnicalStop.TrailingStop import TrailingStop
from Core.Main.Trade.RiskFrameWorks.RiskModeEnum import RiskMode


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

    # region Entry Strategy Stop
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
        self._be.IsPriceInBreakEvenRange(currentPrice, entry, takeProfit)

    def returnFibonnaciTrailing(self,currentPrice: float, stop: float, entry: float) -> float:
        self._trailingStop.returnFibonnaciTrailing(currentPrice, stop, entry)
    # endregion

    #   Implement Profit Stop Analyzer

