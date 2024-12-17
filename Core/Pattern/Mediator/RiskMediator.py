from Core.Main.Trade.RiskFrameWorks.Invalidation.InvalidationClose import InvalidationClose
from Core.Main.Trade.RiskFrameWorks.Invalidation.InvalidationSteady import InvalidationSteady
from Core.Main.Trade.RiskFrameWorks.OrderWeightage.OrderWeightage import OrderWeightage
from Core.Main.Trade.RiskFrameWorks.Ratio.FixedRatio import FixedRatio
from Core.Main.Trade.RiskFrameWorks.Ratio.RangeRatio import RangeRatio
from Core.Main.Trade.RiskFrameWorks.StrategicStop.EndOfmbalance import EndOfImbalance
from Core.Main.Trade.RiskFrameWorks.StrategicStop.OBStop import OBStop
from Core.Main.Trade.RiskFrameWorks.StrategicStop.Swing import SwingStop
from Core.Main.Trade.RiskFrameWorks.TechnicalEntry.CE import CE
from Core.Main.Trade.RiskFrameWorks.TechnicalEntry.Drill import DrillEntry
from Core.Main.Trade.RiskFrameWorks.TechnicalEntry.Fill import FillEntry
from Core.Main.Trade.RiskFrameWorks.TechnicalStop.BreakEven import BreakEven
from Core.Main.Trade.RiskFrameWorks.TechnicalStop.TrailingStop import TrailingStop


class RiskMediator:
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RiskMediator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent re-initialization
            self.invalidationClose: InvalidationClose = InvalidationClose()
            self.invalidationSteady: InvalidationSteady = InvalidationSteady()
            self.orderWeightage: OrderWeightage = OrderWeightage()
            self.fixedRatio: FixedRatio = FixedRatio()
            self.rangeRatio: RangeRatio = RangeRatio()
            self.endOfImbalance: EndOfImbalance = EndOfImbalance()
            self.obStop: OBStop = OBStop()
            self.swingStop: SwingStop= SwingStop()
            self.ce: CE = CE()
            self.drill: DrillEntry = DrillEntry()
            self.fill: FillEntry = FillEntry()
            self.be: BreakEven = BreakEven(0.75)
            self.trailingStop: TrailingStop = TrailingStop()
            self.initialized: bool = True  # Mark as initialized

    def isInvalidationHit(self,riskType,stop,candle,direction) -> bool:
        if riskType == "Close" or riskType == "Steady":
            if riskType == "Close":
                return self.invalidationClose.checkInvalidation(stop, candle, direction)
            if riskType == "Steady":
                return self.invalidationSteady.checkInvalidation(stop, candle, direction)

    def returnSortedTPLevelsToOrders(self,orderAmount: int, tpLevel: list[float], direction: str,mode: int) ->\
            list[tuple[int, float]]:
        return self.orderWeightage.sortOrderToTPLevel(orderAmount,tpLevel,direction,mode)

    def returnPercentagePerLevel(self,percentage: float, order_tp_assignments: list,mode: int) -> list[tuple[int, float, float]]:
        return self.orderWeightage.getPercentagePerLevel(percentage,order_tp_assignments,mode)

    def returnFixedTPLevelByRatio(self,entryPrice,stop,ratio) -> float:
        return self.fixedRatio.getRatio(entryPrice,stop,ratio)

    def returnRangeRatio(self,stop,takeProfits,range)->list:
        return self.rangeRatio.calculateRangeMatrixByStopAndEntry(stop, takeProfits, range)

    def returnImbalanceStop(self,candle)->float:
        return self.endOfImbalance.getStrategyStop(candle)

    def returnSwingStop(self,candle) -> float:
        return self.swingStop.getStrategyStop(candle)

    def returnOBStop(self,candle,mode)->float:
        return self.obStop.getStrategyStop(candle, mode)

    def returnEntryPrice(self,riskType,candle) -> float:
        if riskType == "CE":
            return self.ce.getEntry(candle)

        if riskType == "Drill":
            return self.drill.getEntry(candle)

        if riskType == "Fill":
            return self.fill.getEntry(candle)

    def returnBreakEven(self,currentPrice, entry, takeProfit) -> float:
        return self.be.moveExit(currentPrice, entry, takeProfit)

    def returnTrailingStop(self,currentPrice, stops, currentStop, direction) -> float:
            return self.trailingStop.moveExit(currentPrice, stops, currentStop, direction)
